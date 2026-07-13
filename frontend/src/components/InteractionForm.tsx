import { useState, type FormEvent } from 'react'
import { saveInteraction } from '../api'
import { useAppDispatch, useAppSelector } from '../hooks'
import { resetForm, setField } from '../store'
import type { HCP, InteractionFormState, Sentiment } from '../types'
import HcpSearch from './HcpSearch'

const interactionTypes = [
  'In-person meeting',
  'Virtual meeting',
  'Phone call',
  'Email',
  'Conference',
]

export default function InteractionForm() {
  const form = useAppSelector((state) => state.interaction)
  const dispatch = useAppDispatch()
  const [status, setStatus] = useState<{ kind: 'success' | 'error'; text: string } | null>(null)
  const [isSaving, setIsSaving] = useState(false)

  const update = (field: keyof InteractionFormState, value: string | number | null) => {
    dispatch(setField({ field, value }))
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setStatus(null)
    setIsSaving(true)
    try {
      const saved = await saveInteraction(form)
      setStatus({ kind: 'success', text: `Interaction #${saved.id} saved successfully.` })
      dispatch(resetForm())
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Could not save the interaction.'
      setStatus({ kind: 'error', text: message })
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <section className="panel form-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Interaction details</p>
          <h2>Log HCP Interaction</h2>
        </div>
        <span className="mode-badge">Structured form</span>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid two-columns">
          <HcpSearch
            selectedId={form.hcpId}
            onSelect={(hcp: HCP) => update('hcpId', hcp.id)}
          />
          <div className="field">
            <label htmlFor="interaction-type">Interaction Type</label>
            <select
              id="interaction-type"
              value={form.interactionType}
              onChange={(event) => update('interactionType', event.target.value)}
            >
              {interactionTypes.map((type) => <option key={type}>{type}</option>)}
            </select>
          </div>
        </div>

        <div className="form-grid two-columns">
          <div className="field">
            <label htmlFor="date-time">Date and Time</label>
            <input
              id="date-time"
              type="datetime-local"
              value={form.occurredAt}
              onChange={(event) => update('occurredAt', event.target.value)}
              required
            />
          </div>
          <div className="field">
            <label htmlFor="attendees">Attendees</label>
            <input
              id="attendees"
              value={form.attendees}
              placeholder="Names separated by commas"
              onChange={(event) => update('attendees', event.target.value)}
            />
          </div>
        </div>

        <div className="field">
          <label htmlFor="topics">Topics Discussed</label>
          <textarea
            id="topics"
            value={form.topicsDiscussed}
            placeholder="Products, clinical topics, objections, questions..."
            onChange={(event) => update('topicsDiscussed', event.target.value)}
          />
        </div>

        <div className="field">
          <div className="label-row">
            <label htmlFor="summary">Interaction Summary</label>
            <span>AI-ready notes</span>
          </div>
          <textarea
            id="summary"
            value={form.summary}
            placeholder="Add a factual summary of the discussion..."
            onChange={(event) => update('summary', event.target.value)}
            required
          />
        </div>

        <div className="field">
          <label htmlFor="materials">Materials Shared</label>
          <input
            id="materials"
            value={form.materialsShared}
            placeholder="Clinical overview, study reprint, brochure..."
            onChange={(event) => update('materialsShared', event.target.value)}
          />
          <span className="helper">Separate multiple materials with commas.</span>
        </div>

        <fieldset className="sentiment-fieldset">
          <legend>Observed / Inferred HCP Sentiment</legend>
          <div className="sentiment-options">
            {(['positive', 'neutral', 'negative'] as Sentiment[]).map((sentiment) => (
              <label key={sentiment} className={`sentiment ${form.sentiment === sentiment ? 'active' : ''}`}>
                <input
                  type="radio"
                  name="sentiment"
                  value={sentiment}
                  checked={form.sentiment === sentiment}
                  onChange={() => dispatch(setField({ field: 'sentiment', value: sentiment }))}
                />
                <span>{sentiment === 'positive' ? '◕' : sentiment === 'neutral' ? '●' : '◔'}</span>
                {sentiment}
              </label>
            ))}
          </div>
        </fieldset>

        <div className="field">
          <label htmlFor="outcomes">Outcomes</label>
          <textarea
            id="outcomes"
            value={form.outcomes}
            placeholder="Decisions, commitments, questions to resolve..."
            onChange={(event) => update('outcomes', event.target.value)}
          />
        </div>

        <div className="field">
          <label htmlFor="next-steps">Next Steps / Actions</label>
          <textarea
            id="next-steps"
            value={form.nextSteps}
            placeholder="Follow-up action, owner, timing..."
            onChange={(event) => update('nextSteps', event.target.value)}
          />
        </div>

        {status && <div className={`status ${status.kind}`}>{status.text}</div>}

        <div className="form-actions">
          <button type="button" className="secondary-button" onClick={() => dispatch(resetForm())}>
            Clear
          </button>
          <button type="submit" className="primary-button" disabled={isSaving}>
            {isSaving ? 'Saving...' : 'Save Interaction'}
          </button>
        </div>
      </form>
    </section>
  )
}
