import { useState, useEffect, useRef } from 'react'
import api from '../services/api'

export default function ChatPage() {
  const [customers, setCustomers] = useState([])
  const [selectedCustomer, setSelectedCustomer] = useState(null)
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [loadingCustomers, setLoadingCustomers] = useState(true)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetchCustomers()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchCustomers = async () => {
    try {
      const { data } = await api.getCustomers()
      setCustomers(Array.isArray(data) ? data : data.data || [])
      setLoadingCustomers(false)
    } catch (err) {
      setError('Failed to load customers: ' + (err.message || 'Unknown error'))
      setLoadingCustomers(false)
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || !selectedCustomer || loading) return

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: inputMessage,
      timestamp: new Date().toLocaleTimeString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setLoading(true)
    setError(null)

    try {
      const { data } = await api.chat(selectedCustomer.id, inputMessage)

      const botMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        text: data.reply,
        timestamp: new Date().toLocaleTimeString(),
        approved: data.approved,
        orderId: data.order_id
      }

      setMessages(prev => [...prev, botMessage])
    } catch (err) {
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'error',
        text: 'Error: ' + (err.response?.data?.detail || err.message || 'Failed to send message'),
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, errorMessage])
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col">
      <div className="flex-1 flex gap-4 overflow-hidden">
        {/* Customers Sidebar */}
        <div className="w-64 bg-white shadow-md flex flex-col border-r">
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold text-gray-900">Customers</h2>
          </div>

          {loadingCustomers ? (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                <p className="mt-2 text-gray-600 text-sm">Loading customers...</p>
              </div>
            </div>
          ) : customers.length === 0 ? (
            <div className="flex-1 flex items-center justify-center p-4">
              <div className="text-center">
                <p className="text-gray-500">No customers available</p>
              </div>
            </div>
          ) : (
            <div className="flex-1 overflow-y-auto">
              {customers.map(customer => (
                <button
                  key={customer.id}
                  onClick={() => {
                    setSelectedCustomer(customer)
                    setMessages([])
                  }}
                  className={`w-full text-left px-4 py-3 border-b transition-colors ${
                    selectedCustomer?.id === customer.id
                      ? 'bg-primary-100 border-l-4 border-primary-600'
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="font-medium text-gray-900">{customer.name || 'Customer'}</div>
                  <div className="text-xs text-gray-500">{customer.email || customer.phone || 'No contact'}</div>
                  {customer.is_new_user && (
                    <span className="inline-block mt-1 px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                      New
                    </span>
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col bg-gray-50">
          {!selectedCustomer ? (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <div className="text-5xl mb-4">💬</div>
                <p className="text-gray-600 text-lg">Select a customer to start chatting</p>
              </div>
            </div>
          ) : (
            <>
              {/* Header */}
              <div className="bg-white border-b px-6 py-4 shadow-sm">
                <h2 className="text-xl font-semibold text-gray-900">
                  {selectedCustomer.name || 'Customer'} (ID: {selectedCustomer.id})
                </h2>
                <p className="text-sm text-gray-500">{selectedCustomer.email || selectedCustomer.phone}</p>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800 text-sm">{error}</p>
                  </div>
                )}

                {messages.length === 0 ? (
                  <div className="text-center text-gray-500 py-8">
                    <p>No messages yet. Start the conversation!</p>
                  </div>
                ) : (
                  messages.map(msg => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          msg.sender === 'user'
                            ? 'bg-primary-600 text-white'
                            : msg.sender === 'error'
                            ? 'bg-red-100 text-red-800 border border-red-300'
                            : 'bg-white border border-gray-200'
                        }`}
                      >
                        <p className="text-sm">{msg.text}</p>
                        {msg.approved !== undefined && (
                          <div className="mt-2 pt-2 border-t border-current border-opacity-20">
                            <span className={`text-xs font-semibold ${msg.approved ? 'text-green-600' : 'text-orange-600'}`}>
                              {msg.approved ? '✓ Approved' : '⚠ Needs clarification'}
                            </span>
                            {msg.orderId && (
                              <p className="text-xs mt-1">Order ID: {msg.orderId}</p>
                            )}
                          </div>
                        )}
                        <p className="text-xs opacity-70 mt-1">{msg.timestamp}</p>
                      </div>
                    </div>
                  ))
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input */}
              <form onSubmit={handleSendMessage} className="bg-white border-t p-4 shadow-lg">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    disabled={loading}
                    placeholder="Type your message..."
                    className="flex-1 input-base disabled:bg-gray-100"
                  />
                  <button
                    type="submit"
                    disabled={loading || !inputMessage.trim()}
                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Sending...' : 'Send'}
                  </button>
                </div>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
