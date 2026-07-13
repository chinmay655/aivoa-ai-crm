import AiAssistant from './components/AiAssistant'
import InteractionForm from './components/InteractionForm'

export default function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">A</div>
          <div>
            <strong>AIVOA CRM</strong>
            <span>AI-first field engagement</span>
          </div>
        </div>
        <nav>
          <button type="button">Home</button>
          <button type="button" className="active">Interactions</button>
          <button type="button">HCPs</button>
        </nav>
        <div className="profile">SS</div>
      </header>

      <main>
        <div className="page-intro">
          <div>
            <p className="eyebrow">HCP engagement</p>
            <h1>Log an interaction</h1>
            <p>Capture the conversation with a structured form or ask the AI assistant to do it.</p>
          </div>
          <div className="compliance-note">
            <span>✓</span>
            Structured and traceable
          </div>
        </div>

        <div className="workspace">
          <InteractionForm />
          <AiAssistant />
        </div>
      </main>
    </div>
  )
}
