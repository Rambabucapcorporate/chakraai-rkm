import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { api } from "@/lib/api";

const TYPE_LABELS: Record<string, string> = {
  "1": "Admin", "2": "Student", "3": "Faculty", "4": "Type 4",
  "5": "Type 5", "7": "Type 7", "10": "Type 10", "11": "Type 11",
};

const card = "bg-white rounded-xl border border-gray-200 shadow-sm";

function Bar({ value, max, color }: { value: number; max: number; color: string }) {
  const pct = max > 0 ? Math.min(100, Math.round((value / max) * 100)) : 0;
  return (
    <div className="w-full h-2 rounded-full bg-gray-100 overflow-hidden">
      <div className={`h-full ${color}`} style={{ width: `${pct}%` }} />
    </div>
  );
}

const Admin = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const utype = String((user as any)?.user_type ?? "");
  const isAdmin = utype === "1";

  const [stats, setStats] = useState<any>(null);
  const [gpu, setGpu] = useState<any>(null);
  const [tab, setTab] = useState<"users" | "chats" | "activity">("users");
  const [users, setUsers] = useState<any>(null);
  const [chats, setChats] = useState<any>(null);
  const [activity, setActivity] = useState<any>(null);
  const [userQ, setUserQ] = useState("");
  const [userType, setUserType] = useState("");
  const [chatQ, setChatQ] = useState("");
  const [expanded, setExpanded] = useState<number | null>(null);
  const [err, setErr] = useState<string | null>(null);

  // gate
  useEffect(() => {
    if (user && !isAdmin) navigate("/");
  }, [user, isAdmin, navigate]);

  // stats + live GPU poll
  useEffect(() => {
    if (!isAdmin) return;
    api.admin.stats().then(setStats).catch((e) => setErr(String(e)));
    const pollGpu = () => api.admin.gpu().then(setGpu).catch(() => {});
    pollGpu();
    const iv = setInterval(pollGpu, 5000);
    return () => clearInterval(iv);
  }, [isAdmin]);

  const loadUsers = useCallback(() => {
    api.admin.users(`?q=${encodeURIComponent(userQ)}&user_type=${userType}&limit=100`).then(setUsers).catch(() => {});
  }, [userQ, userType]);
  const loadChats = useCallback(() => {
    api.admin.chats(`?username=${encodeURIComponent(chatQ)}&limit=100`).then(setChats).catch(() => {});
  }, [chatQ]);
  const loadActivity = useCallback(() => {
    api.admin.activity(`?limit=200`).then(setActivity).catch(() => {});
  }, []);

  useEffect(() => {
    if (!isAdmin) return;
    if (tab === "users") loadUsers();
    else if (tab === "chats") loadChats();
    else loadActivity();
  }, [tab, isAdmin, loadUsers, loadChats, loadActivity]);

  if (!user) return <div className="min-h-screen flex items-center justify-center text-gray-500">Loading…</div>;
  if (!isAdmin) return null;

  const StatCard = ({ label, value, sub }: { label: string; value: any; sub?: string }) => (
    <div className={`${card} p-4`}>
      <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide">{label}</div>
      <div className="text-2xl font-bold text-gray-900 mt-1">{value ?? "—"}</div>
      {sub && <div className="text-xs text-gray-400 mt-0.5">{sub}</div>}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* header */}
      <header className="bg-gradient-to-r from-red-800 to-red-600 text-white">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold">RKMVC — Admin Console</h1>
            <p className="text-xs text-white/70">Chakra AI · {user?.username}</p>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={() => navigate("/chat")} className="text-sm px-3 py-1.5 rounded-lg bg-white/15 hover:bg-white/25">Chat</button>
            <button onClick={() => { logout(); navigate("/auth"); }} className="text-sm px-3 py-1.5 rounded-lg bg-white/15 hover:bg-white/25">Logout</button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-6 space-y-6">
        {err && <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">{err}</div>}

        {/* stat cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <StatCard
            label="Active Students Today"
            value={stats?.active_students_today}
            sub={`${stats?.distinct_login_users_today ?? 0} users logged in`}
          />
          <StatCard
            label="Questions Today"
            value={stats?.chats_today}
            sub={`${stats?.active_chat_users_today ?? 0} distinct users`}
          />
          <StatCard
            label="Avg Answer Speed"
            value={stats?.avg_answer_ms_today != null ? `${(stats.avg_answer_ms_today / 1000).toFixed(1)}s` : "—"}
            sub={stats?.answers_measured_today ? `${stats.answers_measured_today} answers today` : "collecting…"}
          />
          <StatCard label="Logins Today" value={stats?.logins_today} />
          <StatCard label="Total Users" value={stats?.total_users} />
          <StatCard label="Active" value={stats?.active_users} />
          <StatCard label="Locked" value={stats?.locked_users} />
          <StatCard label="Chats Total" value={stats?.total_chats} />
        </div>

        {/* GPU health */}
        <section className={`${card} p-5`}>
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-gray-800">GPU Health <span className="text-xs font-normal text-gray-400">· live, refreshes every 5s</span></h2>
            <div className="flex gap-2 text-xs">
              {gpu?.services && Object.entries(gpu.services).map(([s, st]: any) => (
                <span key={s} className={`px-2 py-1 rounded-full font-medium ${st === "active" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>{s}: {st}</span>
              ))}
            </div>
          </div>
          {!gpu?.nvidia_smi_ok && <div className="text-sm text-amber-600">nvidia-smi unavailable</div>}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(gpu?.gpus || []).map((g: any) => {
              const memUsed = Number(g.mem_used_mib), memTot = Number(g.mem_total_mib);
              const util = Number(g.util_pct);
              return (
                <div key={g.index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-semibold text-sm">GPU {g.index} · {g.name}</div>
                    <div className="text-xs text-gray-500">{g.temp_c}°C · {g.power_w}/{g.power_limit_w} W</div>
                  </div>
                  <div className="text-xs text-gray-500 mb-1 flex justify-between"><span>Utilization</span><span>{util}%</span></div>
                  <Bar value={util} max={100} color="bg-blue-500" />
                  <div className="text-xs text-gray-500 mb-1 mt-3 flex justify-between"><span>Memory</span><span>{(memUsed/1024).toFixed(1)} / {(memTot/1024).toFixed(0)} GB</span></div>
                  <Bar value={memUsed} max={memTot} color="bg-red-500" />
                </div>
              );
            })}
          </div>
          {(gpu?.processes?.length > 0) && (
            <div className="mt-4">
              <div className="text-xs font-semibold text-gray-500 uppercase mb-2">GPU Processes</div>
              <div className="flex flex-wrap gap-2">
                {gpu.processes.map((p: any, i: number) => (
                  <span key={i} className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-700">{p.name} · pid {p.pid} · {(Number(p.mem_mib)/1024).toFixed(1)} GB</span>
                ))}
              </div>
            </div>
          )}
        </section>

        {/* tabs */}
        <div className="flex gap-1 border-b border-gray-200">
          {(["users", "chats", "activity"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-2 text-sm font-medium capitalize -mb-px border-b-2 ${tab === t ? "border-red-600 text-red-700" : "border-transparent text-gray-500 hover:text-gray-700"}`}>
              {t === "chats" ? "Chat History" : t === "activity" ? "Activity Log" : "Users"}
            </button>
          ))}
        </div>

        {/* USERS */}
        {tab === "users" && (
          <section className={`${card} p-4`}>
            <div className="flex flex-wrap gap-2 mb-3">
              <input value={userQ} onChange={(e) => setUserQ(e.target.value)} onKeyDown={(e) => e.key === "Enter" && loadUsers()}
                placeholder="Search username…" className="px-3 py-2 border border-gray-300 rounded-lg text-sm flex-1 min-w-[180px]" />
              <select value={userType} onChange={(e) => setUserType(e.target.value)} className="px-3 py-2 border border-gray-300 rounded-lg text-sm">
                <option value="">All types</option>
                {Object.entries(TYPE_LABELS).map(([v, l]) => <option key={v} value={v}>{l}</option>)}
              </select>
              <button onClick={loadUsers} className="px-3 py-2 bg-red-600 text-white rounded-lg text-sm">Search</button>
            </div>
            <div className="text-xs text-gray-400 mb-2">{users?.total ?? 0} users</div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="text-left text-gray-500 border-b border-gray-200">
                  <th className="py-2 pr-4">User ID</th><th className="pr-4">Username</th><th className="pr-4">Type</th>
                  <th className="pr-4">Status</th><th className="pr-4">Last Login</th><th className="pr-4">Locked</th>
                </tr></thead>
                <tbody>
                  {(users?.users || []).map((u: any) => (
                    <tr key={u.userId} className="border-b border-gray-100">
                      <td className="py-2 pr-4 text-gray-400">{u.userId}</td>
                      <td className="pr-4 font-medium">{u.username}</td>
                      <td className="pr-4">{TYPE_LABELS[u.user_type] || u.user_type}</td>
                      <td className="pr-4">{u.status === "1" ? <span className="text-green-600">active</span> : <span className="text-gray-400">inactive</span>}</td>
                      <td className="pr-4 text-gray-500">{u.login_time || "—"}</td>
                      <td className="pr-4">{u.is_locked ? <span className="text-red-600">locked</span> : "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {/* CHATS */}
        {tab === "chats" && (
          <section className={`${card} p-4`}>
            <div className="flex gap-2 mb-3">
              <input value={chatQ} onChange={(e) => setChatQ(e.target.value)} onKeyDown={(e) => e.key === "Enter" && loadChats()}
                placeholder="Filter by username…" className="px-3 py-2 border border-gray-300 rounded-lg text-sm flex-1" />
              <button onClick={loadChats} className="px-3 py-2 bg-red-600 text-white rounded-lg text-sm">Search</button>
            </div>
            <div className="text-xs text-gray-400 mb-2">{chats?.total ?? 0} chats logged</div>
            <div className="space-y-2">
              {(chats?.chats || []).length === 0 && <div className="text-sm text-gray-400 py-6 text-center">No chats yet — they'll appear here as users chat.</div>}
              {(chats?.chats || []).map((c: any) => (
                <div key={c.id} className="border border-gray-200 rounded-lg">
                  <button onClick={() => setExpanded(expanded === c.id ? null : c.id)} className="w-full text-left px-4 py-2.5 flex items-center justify-between hover:bg-gray-50">
                    <div className="min-w-0">
                      <div className="text-sm font-medium truncate">{c.question}</div>
                      <div className="text-xs text-gray-400">{c.username || "anon"} · {c.model} · {c.created_at}</div>
                    </div>
                    <span className="text-gray-400 text-xs ml-2">{expanded === c.id ? "▲" : "▼"}</span>
                  </button>
                  {expanded === c.id && (
                    <div className="px-4 py-3 border-t border-gray-100 bg-gray-50">
                      <div className="text-xs font-semibold text-gray-500 mb-1">Answer</div>
                      <div className="text-sm text-gray-700 whitespace-pre-wrap max-h-96 overflow-y-auto">{c.answer}</div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* ACTIVITY */}
        {tab === "activity" && (
          <section className={`${card} p-4`}>
            <div className="text-xs text-gray-400 mb-2">{activity?.total ?? 0} events</div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="text-left text-gray-500 border-b border-gray-200">
                  <th className="py-2 pr-4">Time</th><th className="pr-4">User</th><th className="pr-4">Action</th><th className="pr-4">Detail</th>
                </tr></thead>
                <tbody>
                  {(activity?.activity || []).map((a: any) => (
                    <tr key={a.id} className="border-b border-gray-100">
                      <td className="py-2 pr-4 text-gray-500">{a.created_at}</td>
                      <td className="pr-4 font-medium">{a.username || "—"}</td>
                      <td className="pr-4">
                        <span className={`px-2 py-0.5 rounded-full text-xs ${a.action === "login" ? "bg-blue-100 text-blue-700" : "bg-purple-100 text-purple-700"}`}>{a.action}</span>
                      </td>
                      <td className="pr-4 text-gray-500 truncate max-w-md">{a.detail}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default Admin;
