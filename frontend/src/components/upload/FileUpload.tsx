'use client'
import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { 
  DocumentArrowUpIcon, 
  CheckCircleIcon, 
  XCircleIcon 
} from '@heroicons/react/24/outline'

interface FileUploadProps {
  onFileUpload: (file: File, type: 'calendar' | 'timetable') => void
  uploadType: 'calendar' | 'timetable'
  title: string
  description: string
}

export default function FileUpload({ 
  onFileUpload, 
  uploadType, 
  title, 
  description 
}: FileUploadProps) {
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle')
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0]
      setUploadedFile(file)
      setUploadStatus('uploading')
      
      // Simulate upload process
      setTimeout(() => {
        onFileUpload(file, uploadType)
        setUploadStatus('success')
      }, 2000)
    }
  }, [onFileUpload, uploadType])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    maxFiles: 1
  })

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white rounded-xl shadow-lg p-6 border border-gray-200"
    >
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 mb-6">{description}</p>

      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all
          ${isDragActive 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'
          }
          ${uploadStatus === 'success' ? 'border-green-400 bg-green-50' : ''}
          ${uploadStatus === 'error' ? 'border-red-400 bg-red-50' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          {uploadStatus === 'success' ? (
            <CheckCircleIcon className="h-12 w-12 text-green-500" />
          ) : uploadStatus === 'error' ? (
            <XCircleIcon className="h-12 w-12 text-red-500" />
          ) : (
            <DocumentArrowUpIcon className="h-12 w-12 text-gray-400" />
          )}

          <div>
            {uploadStatus === 'uploading' && (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                <span className="text-blue-600">Processing...</span>
              </div>
            )}
            
            {uploadStatus === 'success' && uploadedFile && (
              <div className="text-green-600">
                <div className="font-semibold">✓ Upload Complete</div>
                <div className="text-sm">{uploadedFile.name}</div>
              </div>
            )}
            
            {uploadStatus === 'idle' && (
              <div className="text-gray-600">
                <div className="font-semibold">
                  {isDragActive ? 'Drop file here' : 'Click to upload or drag and drop'}
                </div>
                <div className="text-sm">PDF, PNG, JPG up to 10MB</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  )
}