#ifndef _MPTCPLIB_LINUX
#define _MPTCPLIB_LINUX

#include <sys/types.h>
#include <sys/socket.h>
#include <stdbool.h>
#include <linux/tcp.h>
#include <linux/types.h>

#ifndef SOL_MPTCP
#define SOL_MPTCP 284
#endif

#define MPTCPLIB_OPERATION_UNSUPPORTED -2
#define MPTCPLIB_SOCKET_FALLBACK_TCP -1
#define MPTCPLIB_ERROR_FLAG -3

#ifndef MPTCP_INFO
#define MPTCP_INFO 1
struct mptcp_info {
	__u8	mptcpi_subflows;
	__u8	mptcpi_add_addr_signal;
	__u8	mptcpi_add_addr_accepted;
	__u8	mptcpi_subflows_max;
	__u8	mptcpi_add_addr_signal_max;
	__u8	mptcpi_add_addr_accepted_max;
	__u32	mptcpi_flags;
	__u32	mptcpi_token;
	__u64	mptcpi_write_seq;
	__u64	mptcpi_snd_una;
	__u64	mptcpi_rcv_nxt;
	__u8	mptcpi_local_addr_used;
	__u8	mptcpi_local_addr_max;
	__u8	mptcpi_csum_enabled;
};

#endif

#endif /*_MPTCP_PYLIB*/