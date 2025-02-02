/*
 * MIT License
 *
 * Copyright (c) 2020-2024 EntySec
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/*! \file core.h
 *  \brief control core entry point to a main event loop
 */

#ifndef _CORE_H_
#define _CORE_H_

#include <pwny/c2.h>
#include <pwny/tlv.h>
#include <ev.h>
#include <sigar.h>
#include <pwny/tabs.h>
#include <pwny/pipe.h>
#include <pwny/tunnel.h>

#define CORE_EV_FLAGS EVFLAG_NOENV | EVBACKEND_SELECT | EVFLAG_FORKCHECK

#define CORE_INJECTED 1 /* let code know that core was injected */
#ifdef __linux__
#define CORE_NO_DUMP  2 /* attempt to make process non dumpable */
#define CORE_NO_NAME  3 /* attempt to hide process name */
#endif

typedef struct
{
    c2_t *c2;
    sigar_t *sigar;
    char *path;
    char *uuid;

    int t_count;
    int c_count;
    int flags;

    tabs_t *tabs;
    api_calls_t *api_calls;
    tunnels_t *tunnels;

    struct ev_loop *loop;
} core_t;

core_t *core_create(void);

void core_set_path(core_t *core, char *path);
void core_set_uuid(core_t *core, char *uuid);

int core_add_uri(core_t *core, char *uri);

void core_setup(core_t *core);
int core_start(core_t *core);

void core_destroy(core_t *core);

#endif