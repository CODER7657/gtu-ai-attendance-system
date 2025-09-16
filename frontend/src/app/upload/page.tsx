'use client'
import { useState } from 'react'
import { motion } from 'framer-motion'
import Navbar from '@/components/layout/Navbar'
import FileUpload from '@/components/upload/FileUpload'
import { apiService } from '@/services/api'

export default function UploadPage() {
  const [uploadedFiles, setUploadedFiles] = useState<{
    calendar?: File
    timetable?: File
  }>({})
  const [preferences, setPreferences] = useState('')
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState(1)

  const handleFileUpload = async (file: File, type: 'calendar' | 'timetable') => {
    try {
      setLoading(true)
      const response = await apiService.uploadFile(file, type)
      
      setUploadedFiles(prev => ({
        ...prev,
        [type]: file
      }))
      
      console.log('Upload successful:', response)
    } catch (error) {
      console.error('Upload failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePreferencesSubmit = async () => {
    if (!preferences.trim()) {
      alert('Please enter your preferences')
      return
    }

    try {
      setLoading(true)
      const response = await apiService.savePreferences(preferences)
      console.log('Preferences saved:', response)
      
      // Move to next step or redirect to dashboard
      alert('Setup complete! Redirecting to dashboard...')
      window.location.href = '/dashboard'
    } catch (error) {
      console.error('Failed to save preferences:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Navbar />
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-8"
        >
          {/* Progress Indicator */}
          <div className="flex items-center justify-center space-x-4 mb-8">
            {[1, 2, 3].map((stepNumber) => (
              <div key={stepNumber} className="flex items-center">
                <div className={`
                  w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold
                  ${step >= stepNumber ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'}
                `}>
                  {stepNumber}
                </div>
                {stepNumber < 3 && (
                  <div className={`w-12 h-0.5 mx-2 ${
                    step > stepNumber ? 'bg-blue-600' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>

          {/* Step 1: Upload Calendar */}
          {step === 1 && (
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-6"
            >
              <div className="text-center">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Upload Your Academic Calendar</h1>
                <p className="text-gray-600">Upload your college's academic calendar PDF to extract working days and holidays</p>
              </div>
              
              <FileUpload
                onFileUpload={handleFileUpload}
                uploadType="calendar"
                title="Academic Calendar"
                description="Upload your college's official academic calendar (PDF or image format)"
              />

              {uploadedFiles.calendar && (
                <div className="text-center">
                  <button
                    onClick={() => setStep(2)}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                  >
                    Continue to Timetable Upload
                  </button>
                </div>
              )}
            </motion.div>
          )}

          {/* Step 2: Upload Timetable */}
          {step === 2 && (
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-6"
            >
              <div className="text-center">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Upload Your Timetable</h1>
                <p className="text-gray-600">Upload your class timetable to track subject-wise attendance</p>
              </div>
              
              <FileUpload
                onFileUpload={handleFileUpload}
                uploadType="timetable"
                title="Class Timetable"
                description="Upload your weekly class timetable (PDF or image format)"
              />

              {uploadedFiles.timetable && (
                <div className="text-center">
                  <button
                    onClick={() => setStep(3)}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                  >
                    Continue to Preferences
                  </button>
                </div>
              )}
            </motion.div>
          )}

          {/* Step 3: Preferences */}
          {step === 3 && (
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-6"
            >
              <div className="text-center">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Tell Us Your Preferences</h1>
                <p className="text-gray-600">Share your subject preferences so our AI can give you personalized recommendations</p>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Describe your preferences (e.g., "I love Mathematics but hate early morning classes. Physics is boring but Chemistry practicals are interesting.")
                </label>
                <textarea
                  value={preferences}
                  onChange={(e) => setPreferences(e.target.value)}
                  rows={6}
                  className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Tell us about your subject preferences, favorite/disliked times, and any other attendance-related preferences..."
                />
                
                <div className="mt-6 text-center">
                  <button
                    onClick={handlePreferencesSubmit}
                    disabled={loading}
                    className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50"
                  >
                    {loading ? 'Processing...' : 'Complete Setup'}
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>
      </main>
    </>
  )
}