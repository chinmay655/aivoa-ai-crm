import axios from 'axios'
import type { HCP, InteractionFormState } from './types'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
  timeout: 30000,
})

export async function searchHcps(query = ''): Promise<HCP[]> {
  const response = await client.get<HCP[]>('/api/hcps', { params: { q: query } })
  return response.data
}

export async function saveInteraction(form: InteractionFormState) {
  if (!form.hcpId) {
    throw new Error('Select an HCP before saving.')
  }

  const response = await client.post('/api/interactions', {
    hcp_id: form.hcpId,
    interaction_type: form.interactionType,
    occurred_at: new Date(form.occurredAt).toISOString(),
    attendees: form.attendees
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean),
    topics_discussed: form.topicsDiscussed,
    summary: form.summary,
    materials_shared: form.materialsShared
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean),
    sentiment: form.sentiment,
    outcomes: form.outcomes,
    next_steps: form.nextSteps,
  })
  return response.data
}

export async function sendAgentMessage(message: string) {
  const response = await client.post<{ response: string; tools_used: string[] }>(
    '/api/agent/chat',
    { message },
  )
  return response.data
}
