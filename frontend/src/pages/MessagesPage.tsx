import { FormEvent, useEffect, useState } from 'react';

import { runMessageAgent } from '../api/agents';
import { fetchConversationMessages, fetchConversations, sendMessage } from '../api/messages';
import { PageHeader } from '../components/ui/PageHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import type { MessageAgentResult } from '../types/agent';
import type { Conversation, Message } from '../types/message';

export function MessagesPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [reply, setReply] = useState('');
  const [agentResult, setAgentResult] = useState<MessageAgentResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [runningAgent, setRunningAgent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadConversations = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchConversations();
      setConversations(data);
      if (!selectedConversation && data[0]) {
        setSelectedConversation(data[0]);
      }
    } catch {
      setError('Unable to load WhatsApp conversations.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadConversations();
  }, []);

  useEffect(() => {
    if (!selectedConversation) return;

    fetchConversationMessages(selectedConversation.customer_id)
      .then((data) => {
        setMessages(data);
        setAgentResult(null);
      })
      .catch(() => setError('Unable to load conversation history.'));
  }, [selectedConversation]);

  const handleSend = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedConversation || !reply.trim()) return;

    setSending(true);
    setError(null);
    try {
      const sentMessage = await sendMessage(selectedConversation.customer_id, reply.trim());
      setMessages((current) => [...current, sentMessage]);
      setReply('');
      await loadConversations();
    } catch {
      setError('Unable to send WhatsApp reply.');
    } finally {
      setSending(false);
    }
  };

  const handleRunAgent = async () => {
    const latestInbound = [...messages].reverse().find((message) => message.direction === 'inbound');
    if (!latestInbound) {
      setError('No inbound message is available for the AI agent.');
      return;
    }

    setRunningAgent(true);
    setError(null);
    try {
      const result = await runMessageAgent(latestInbound.id);
      setAgentResult(result);
      if (result.suggested_reply && !result.sent_message_id) {
        setReply(result.suggested_reply);
      }
      if (selectedConversation) {
        setMessages(await fetchConversationMessages(selectedConversation.customer_id));
      }
    } catch {
      setError('Unable to run the AI message agent.');
    } finally {
      setRunningAgent(false);
    }
  };

  return (
    <section className="mx-auto max-w-7xl space-y-6">
      <PageHeader title="Messages" description="WhatsApp conversations, history, and outbound replies." />

      {error && <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

      <div className="grid gap-4 lg:grid-cols-[340px_1fr]">
        <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
          {loading && <div className="p-4 text-sm text-slate-600">Loading conversations...</div>}
          {!loading && conversations.length === 0 && (
            <div className="p-4 text-sm text-slate-600">No WhatsApp conversations yet.</div>
          )}
          {conversations.map((conversation) => (
            <button
              key={conversation.customer_id}
              type="button"
              onClick={() => setSelectedConversation(conversation)}
              className={[
                'block w-full border-b border-slate-100 px-4 py-4 text-left hover:bg-slate-50',
                selectedConversation?.customer_id === conversation.customer_id ? 'bg-cyan-50' : '',
              ].join(' ')}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="font-medium text-slate-950">{conversation.customer_name}</p>
                  <p className="mt-1 truncate text-sm text-slate-600">{conversation.last_message}</p>
                  <p className="mt-1 text-xs text-slate-500">{conversation.phone}</p>
                </div>
                <div className="shrink-0 text-right">
                  <StatusBadge label={conversation.status} />
                  {conversation.unread_count > 0 && (
                    <p className="mt-2 text-xs font-semibold text-red-700">
                      {conversation.unread_count} unread
                    </p>
                  )}
                </div>
              </div>
            </button>
          ))}
        </div>

        <div className="flex min-h-[520px] flex-col rounded-lg border border-slate-200 bg-white shadow-sm">
          {selectedConversation ? (
            <>
              <div className="border-b border-slate-200 p-5">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="font-semibold text-slate-950">{selectedConversation.customer_name}</p>
                    <p className="text-sm text-slate-500">WhatsApp · {selectedConversation.phone}</p>
                  </div>
                  <button
                    type="button"
                    onClick={handleRunAgent}
                    disabled={runningAgent}
                    className="rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 disabled:opacity-50"
                  >
                    {runningAgent ? 'Running AI...' : 'Run AI agent'}
                  </button>
                </div>
                {agentResult && (
                  <div className="mt-4 rounded-md border border-cyan-200 bg-cyan-50 p-3 text-sm text-cyan-900">
                    <p className="font-semibold">
                      {agentResult.intent ?? 'unknown'} · confidence{' '}
                      {Math.round((agentResult.confidence_score ?? 0) * 100)}%
                    </p>
                    <p className="mt-1">{agentResult.ai_reasoning}</p>
                  </div>
                )}
              </div>
              <div className="flex-1 space-y-4 overflow-y-auto p-5">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={[
                      'max-w-xl rounded-lg px-4 py-3 text-sm',
                      message.direction === 'outbound'
                        ? 'ml-auto bg-cyan-700 text-white'
                        : 'bg-slate-100 text-slate-700',
                    ].join(' ')}
                  >
                    <p>{message.body}</p>
                    <p className={message.direction === 'outbound' ? 'mt-2 text-xs text-cyan-100' : 'mt-2 text-xs text-slate-500'}>
                      {message.status} · {new Date(message.created_at).toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>
              <form onSubmit={handleSend} className="border-t border-slate-200 p-4">
                <div className="flex flex-col gap-3 sm:flex-row">
                  <input
                    className="min-h-11 flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm"
                    placeholder="Type a WhatsApp reply"
                    value={reply}
                    onChange={(event) => setReply(event.target.value)}
                  />
                  <button
                    type="submit"
                    disabled={sending || !reply.trim()}
                    className="rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white disabled:bg-slate-400"
                  >
                    {sending ? 'Sending...' : 'Send'}
                  </button>
                </div>
              </form>
            </>
          ) : (
            <div className="flex flex-1 items-center justify-center p-5 text-sm text-slate-600">
              Select a conversation to view message history.
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
