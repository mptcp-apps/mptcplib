#include <Python.h>
#include "_mptcplib_linux.h"
#include <errno.h>

static PyObject *Mptcplib_Error;

/* Patch from https://github.com/multipath-tcp/mptcp_net-next/issues/294#issuecomment-1301920288 */
int
Csocket_is_mptcp(int sockfd)
{
	socklen_t len;
	bool val;
	len = sizeof(val);
	/* We should get EOPNOTSUPP in case of fallback */
	if (getsockopt(sockfd, SOL_MPTCP, MPTCP_INFO, &val, &len) < 0){
		if (errno != EOPNOTSUPP){
			PyErr_Format(Mptcplib_Error, "The socket getsockopt returned %d", errno);
			return MPTCPLIB_ERROR_FLAG;
		}
		return MPTCPLIB_SOCKET_FALLBACK_TCP;
	}
	/* no error: MPTCP is supported */
	return 0;
}

static PyObject* socket_is_mptcp(PyObject* self, PyObject* args)
{
	int sockfd ;
	if (!PyArg_ParseTuple(args, "i", &sockfd))		return NULL;
	if (sockfd <= 0){
		PyErr_SetString(Mptcplib_Error, "The socket file descriptor given to 'socket_is_mptcp' is less or equal to zero");
		return NULL;
	}				
	int returned_value = Csocket_is_mptcp(sockfd);
	if (returned_value == MPTCPLIB_ERROR_FLAG)		return NULL;			
	return Py_BuildValue("i", returned_value);
}

int
Cused_subflows(int sockfd)
{
	int socket_is_mptcp_returned = Csocket_is_mptcp(sockfd);
	if ( socket_is_mptcp_returned == 0 ){
		struct mptcp_info inf;
		socklen_t optlen;
		optlen = sizeof(inf);
		if (!getsockopt(sockfd, SOL_MPTCP, MPTCP_INFO, &inf, &optlen)) {
			return inf.mptcpi_subflows;
		} else {
			PyErr_Format(Mptcplib_Error, "The socket getsockopt returned %d", errno);
		}
	}
	return MPTCPLIB_SOCKET_FALLBACK_TCP;
}

static PyObject* used_subflows(PyObject* self, PyObject* args)
{
	int sockfd;
	if (!PyArg_ParseTuple(args, "i", &sockfd))		return NULL;
	if (sockfd <= 0){
		PyErr_SetString(Mptcplib_Error, "The socket file descriptor given to 'used_subflows' is less or equal to zero.");
		return NULL;
	}								
	int value_returned = Cused_subflows(sockfd);
	if (value_returned != MPTCPLIB_ERROR_FLAG){
		return Py_BuildValue("i", value_returned);
	} else if (value_returned == MPTCPLIB_ERROR_FLAG){
		PyErr_Format(Mptcplib_Error, "getseckopt returned errno with code %d.", errno);
		return NULL;
	} else {
		return Py_BuildValue("i", value_returned);
	}
}

static PyMethodDef mptcplibMethods[] = {
	{"socket_is_mptcp", socket_is_mptcp, METH_VARARGS, "Checks if the socket is an mptcp socket."}, 
	{"used_subflows", used_subflows, METH_VARARGS, "Returns the number of subflows used for the MPTCP connection."},
	{NULL, NULL, 0, NULL}  /* Sentinel */
};

static struct PyModuleDef mptcplib_module = {
	PyModuleDef_HEAD_INIT,
	"_mptcplib_linux", 
	"Multipath TCP CPython lib", 
	-1, 
	mptcplibMethods
};

PyMODINIT_FUNC PyInit__mptcplib_linux(void)
{
	PyObject *module;
	module = PyModule_Create(&mptcplib_module);
	if (module == NULL)
		return NULL;
	Mptcplib_Error = PyErr_NewException("mptcplib.Error", NULL, NULL);
	Py_XINCREF(Mptcplib_Error);
	if (PyModule_AddObject(module, "error", Mptcplib_Error) < 0) {
        Py_XDECREF(Mptcplib_Error);
        Py_CLEAR(Mptcplib_Error);
        Py_DECREF(module);
        return NULL;
    }
	return module;
}