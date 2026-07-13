import { useState, type FormEvent } from 'react'
import { sendAgentMessage } from '../api'
import { useAppDispatch, useAppSelector } from '../hooks'
import { addMessage, setSending } from '../store'

const suggestions = [
  'Find Dr. Sarah Mitchell',
  'Show interaction history for Dr. Sarah Mitchell',
  'Log a phone call with Dr. Michael Chen',
]

const createId = () => `${Date.now()}-${Math.random().toString(16).slice(2)}`

export default function AiAssistant() {
  const { messages, isSending } = useAppSelector((state) => state.chat)
  const dispatch = useAppDispatch()
  const [input, setInput] = useState('')

  const submit = async (message: string) => {
    const cleaned = message.trim()
    if (!cleaned || isSending) return

    dispatch(addMessage({ id: createId(), role: 'user', content: cleaned }))
    setInput('')
    dispatch(setSending(true))

    try {
      const result = await sendAgentMessage(cleaned)
      dispatch(
        addMessage({
          id: createId(),
          role: 'assistant',
          content: result.response,
          toolsUsed: result.tools_used,
        }),
      )
    } catch (error: unknown) {
      let content = 'The assistant could not complete that request.'
      if (typeof error === 'object' && error !== null && 'response' in error) {
        const response = (error as { response?: { data?: { detail?: string } } }).response
        content = response?.data?.detail ?? content
      }
      dispatch(addMessage({ id: createId(), role: 'assistant', content }))
    } finally {
      dispatch(setSending(false))
    }
  }

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    void submit(input)
  }

  return (
    <aside className="panel assistant-panel">
      <div className="assistant-header">
        <div className="assistant-icon">AI</div>
        <div>
          <h2>AI Assistant</h2>
          <p>LangGraph CRM copilot</p>
        </div>
        <span className="online-dot" title="Ready" />
      </div>

      <div className="chat-feed">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <p>{message.content}</p>
            {!!message.toolsUsed?.length && (
              <div className="tool-chips">
                {message.toolsUsed.map((tool) => <span key={tool}>{tool}</span>)}
              </div>
            )}
          </div>
        ))}
        {isSending && <div className="message assistant typing">Thinking<span>...</span></div>}
      </div>

      <div className="suggestions">
        {suggestions.map((suggestion) => (
          <button key={suggestion} type="button" onClick={() => void submit(suggestion)}>
            {suggestion}
          </button>
        ))}
      </div>

      <form className="chat-composer" onSubmit={handleSubmit}>
        <textarea
          value={input}
          placeholder="Describe the interaction or ask the assistant to take an action..."
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault()
              void submit(input)
            }
          }}
        />
        <button type="submit" disabled={!input.trim() || isSending} aria-label="Send message">
          Send
        </button>
      </form>
      <p className="disclaimer">Do not enter patient-identifying information.</p>
    </aside>
  )
}
