import { configureStore, createSlice, type PayloadAction } from '@reduxjs/toolkit'
import type { ChatMessage, InteractionFormState, Sentiment } from './types'

const localDateTime = () => {
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  return now.toISOString().slice(0, 16)
}

const initialForm: InteractionFormState = {
  hcpId: null,
  interactionType: 'In-person meeting',
  occurredAt: localDateTime(),
  attendees: '',
  topicsDiscussed: '',
  summary: '',
  materialsShared: '',
  sentiment: 'neutral',
  outcomes: '',
  nextSteps: '',
}

const interactionSlice = createSlice({
  name: 'interaction',
  initialState: initialForm,
  reducers: {
    setField: (
      state,
      action: PayloadAction<{
        field: keyof InteractionFormState
        value: string | number | null | Sentiment
      }>,
    ) => {
      const { field, value } = action.payload
      ;(state[field] as typeof value) = value
    },
    resetForm: () => ({ ...initialForm, occurredAt: localDateTime() }),
  },
})

const initialMessages: ChatMessage[] = [
  {
    id: 'welcome',
    role: 'assistant',
    content:
      'Tell me what you need to do. I can search HCPs, log or edit interactions, add samples, schedule follow-ups, and retrieve interaction history.',
  },
]

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: initialMessages,
    isSending: false,
  },
  reducers: {
    addMessage: (state, action: PayloadAction<ChatMessage>) => {
      state.messages.push(action.payload)
    },
    setSending: (state, action: PayloadAction<boolean>) => {
      state.isSending = action.payload
    },
  },
})

export const { setField, resetForm } = interactionSlice.actions
export const { addMessage, setSending } = chatSlice.actions

export const store = configureStore({
  reducer: {
    interaction: interactionSlice.reducer,
    chat: chatSlice.reducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
