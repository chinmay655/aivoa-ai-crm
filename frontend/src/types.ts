export type Sentiment = 'positive' | 'neutral' | 'negative'

export interface HCP {
  id: number
  name: string
  specialty: string
  organization: string
  city: string
  state: string
  email?: string | null
}

export interface InteractionFormState {
  hcpId: number | null
  interactionType: string
  occurredAt: string
  attendees: string
  topicsDiscussed: string
  summary: string
  materialsShared: string
  sentiment: Sentiment
  outcomes: string
  nextSteps: string
}

export interface ChatMessage {
  id: string
  role: 'assistant' | 'user'
  content: string
  toolsUsed?: string[]
}
