'use client'
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  ChartBarIcon, 
  ExclamationTriangleIcon, 
  CheckCircleIcon,
  ClockIcon,
  AcademicCapIcon,
  TrophyIcon,
  CalendarDaysIcon
} from '@heroicons/react/24/outline'

interface GTUAttendanceData {
  currentPercentage: number
  totalClasses: number
  attendedClasses: number
  remainingWeeks: number
  examEligible: boolean
  bonusEligible: boolean
  bonusMarks: {
    attendance: number
    firstFourDays: number
    allClear: number
    total: number
  }
  subjects: {
    [key: string]: {
      name: string
      attendance: number
      weeklyClasses: number
      type: 'liked' | 'disliked' | 'neutral'
    }
  }
  warnings: string[]
  scenarios: {
    [key: string]: {
      requiredToAttend: number
      remainingClasses: number
      canSkip: number
      finalAttendance: number
    }
  }
}

interface GTUPolicyCard {
  title: string
  value: string | number
  status: 'safe' | 'warning' | 'critical' | 'excellent'
  description: string
  icon: React.ComponentType<any>
}

export default function GTUDashboard() {
  const [attendanceData, setAttendanceData] = useState<GTUAttendanceData | null>(null)
  const [selectedScenario, setSelectedScenario] = useState('maintain_current')
  const [rollNumber, setRollNumber] = useState<number>(25)
  const [loading, setLoading] = useState(true)

  // Sample GTU data based on your situation
  const sampleGTUData: GTUAttendanceData = {
    currentPercentage: 72.0,
    totalClasses: 190,
    attendedClasses: 137,
    remainingWeeks: 10,
    examEligible: true,
    bonusEligible: true,
    bonusMarks: {
      attendance: 11, // (72/100) * 15 = 10.8 ≈ 11
      firstFourDays: 4, // Assuming attended first 4 days
      allClear: 0, // Only if all subjects clear after bonuses
      total: 15
    },
    subjects: {
      'DS': { name: 'Data Structures', attendance: 85, weeklyClasses: 4, type: 'liked' },
      'DBMS': { name: 'Database Management System', attendance: 80, weeklyClasses: 4, type: 'liked' },
      'PS': { name: 'Probability and Statistics', attendance: 75, weeklyClasses: 3, type: 'liked' },
      'DF': { name: 'Digital Fundamentals', attendance: 70, weeklyClasses: 4, type: 'neutral' },
      'IC': { name: 'Indian Constitution', attendance: 55, weeklyClasses: 2, type: 'disliked' },
      'PCE': { name: 'Professional Communication and Ethics', attendance: 60, weeklyClasses: 2, type: 'disliked' }
    },
    warnings: [
      '✅ SAFE: Currently eligible for exams and bonus marks',
      '⚠️ CAUTION: IC and PCE below ideal levels - consider strategic attendance'
    ],
    scenarios: {
      'maintain_current': { requiredToAttend: 137, remainingClasses: 190, canSkip: 53, finalAttendance: 72.0 },
      'safe_buffer': { requiredToAttend: 150, remainingClasses: 190, canSkip: 40, finalAttendance: 75.0 },
      'bonus_optimization': { requiredToAttend: 160, remainingClasses: 190, canSkip: 30, finalAttendance: 80.0 },
      'minimum_safe': { requiredToAttend: 134, remainingClasses: 190, canSkip: 56, finalAttendance: 70.1 }
    }
  }

  useEffect(() => {
    // Simulate loading GTU data
    setTimeout(() => {
      setAttendanceData(sampleGTUData)
      setLoading(false)
    }, 1500)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'safe': return 'text-green-600 bg-green-100'
      case 'excellent': return 'text-blue-600 bg-blue-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'critical': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getPolicyCards = (): GTUPolicyCard[] => {
    if (!attendanceData) return []

    return [
      {
        title: 'GTU Exam Eligibility',
        value: attendanceData.examEligible ? '✅ Eligible' : '❌ Not Eligible',
        status: attendanceData.examEligible ? 'safe' : 'critical',
        description: `${attendanceData.currentPercentage}% (Need 70%+ for GTU exams)`,
        icon: AcademicCapIcon
      },
      {
        title: 'Bonus Marks Potential',
        value: `${attendanceData.bonusMarks.total} marks`,
        status: attendanceData.bonusMarks.total > 15 ? 'excellent' : attendanceData.bonusMarks.total > 10 ? 'safe' : 'warning',
        description: `${attendanceData.bonusMarks.attendance} (attendance) + ${attendanceData.bonusMarks.firstFourDays} (first 4 days)`,
        icon: TrophyIcon
      },
      {
        title: 'Remaining Buffer',
        value: `${attendanceData.currentPercentage - 70}%`,
        status: (attendanceData.currentPercentage - 70) > 5 ? 'safe' : (attendanceData.currentPercentage - 70) > 2 ? 'warning' : 'critical',
        description: 'Safety margin above 70% minimum',
        icon: ExclamationTriangleIcon
      },
      {
        title: 'Division Assignment',
        value: rollNumber <= 35 ? 'DIV-9' : 'DIV-10',
        status: 'safe',
        description: `Roll ${rollNumber} (${rollNumber <= 35 ? '1-35' : '36-69'})`,
        icon: CalendarDaysIcon
      }
    ]
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600"></div>
          </div>
        </div>
      </div>
    )
  }

  const policyCards = getPolicyCards()
  const currentScenario = attendanceData?.scenarios[selectedScenario]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            GTU SEM-3 CSE(DS) Dashboard
          </h1>
          <p className="text-gray-600">
            Your comprehensive attendance tracking with GTU policy compliance
          </p>
          
          {/* Roll Number Input */}
          <div className="mt-4 flex justify-center">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-gray-700">Roll Number:</label>
              <input
                type="number"
                min="1"
                max="69"
                value={rollNumber}
                onChange={(e) => setRollNumber(Number(e.target.value))}
                className="w-20 px-2 py-1 border border-gray-300 rounded-md text-center"
              />
              <span className="text-sm text-gray-500">
                ({rollNumber <= 35 ? 'DIV-9' : 'DIV-10'})
              </span>
            </div>
          </div>
        </motion.div>

        {/* Policy Status Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {policyCards.map((card, index) => (
            <div key={index} className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-3">
                <card.icon className="h-6 w-6 text-blue-600" />
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusColor(card.status)}`}>
                  {card.status.toUpperCase()}
                </span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-1">{card.title}</h3>
              <p className="text-2xl font-bold text-gray-900 mb-2">{card.value}</p>
              <p className="text-sm text-gray-600">{card.description}</p>
            </div>
          ))}
        </motion.div>

        {/* Subject-wise Attendance */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">SEM-3 Subject Attendance</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {attendanceData && Object.entries(attendanceData.subjects).map(([code, subject]) => (
              <div key={code} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-gray-900">{code}</h3>
                    <p className="text-sm text-gray-600">{subject.name}</p>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${
                    subject.type === 'liked' ? 'bg-green-100 text-green-800' :
                    subject.type === 'disliked' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {subject.type}
                  </span>
                </div>
                <div className="mb-2">
                  <div className="flex justify-between text-sm mb-1">
                    <span>Attendance</span>
                    <span className={`font-semibold ${
                      subject.attendance >= 80 ? 'text-green-600' :
                      subject.attendance >= 70 ? 'text-yellow-600' :
                      'text-red-600'
                    }`}>
                      {subject.attendance}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        subject.attendance >= 80 ? 'bg-green-500' :
                        subject.attendance >= 70 ? 'bg-yellow-500' :
                        'bg-red-500'
                      }`}
                      style={{ width: `${subject.attendance}%` }}
                    ></div>
                  </div>
                </div>
                <p className="text-xs text-gray-500">{subject.weeklyClasses} classes/week</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Attendance Scenarios */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Attendance Strategy Scenarios</h2>
          
          {/* Scenario Selector */}
          <div className="mb-6">
            <div className="flex flex-wrap gap-2">
              {attendanceData && Object.entries(attendanceData.scenarios).map(([key, scenario]) => (
                <button
                  key={key}
                  onClick={() => setSelectedScenario(key)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedScenario === key
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </button>
              ))}
            </div>
          </div>

          {/* Selected Scenario Details */}
          {currentScenario && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="font-semibold text-blue-900">Required Classes</h3>
                <p className="text-2xl font-bold text-blue-600">{currentScenario.requiredToAttend}</p>
                <p className="text-sm text-blue-700">out of {currentScenario.remainingClasses} remaining</p>
              </div>
              <div className="bg-green-50 rounded-lg p-4">
                <h3 className="font-semibold text-green-900">Can Skip</h3>
                <p className="text-2xl font-bold text-green-600">{currentScenario.canSkip}</p>
                <p className="text-sm text-green-700">classes safely</p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <h3 className="font-semibold text-purple-900">Final Attendance</h3>
                <p className="text-2xl font-bold text-purple-600">{currentScenario.finalAttendance.toFixed(1)}%</p>
                <p className="text-sm text-purple-700">projected</p>
              </div>
              <div className="bg-yellow-50 rounded-lg p-4">
                <h3 className="font-semibold text-yellow-900">Safety Buffer</h3>
                <p className="text-2xl font-bold text-yellow-600">{(currentScenario.finalAttendance - 70).toFixed(1)}%</p>
                <p className="text-sm text-yellow-700">above minimum</p>
              </div>
            </div>
          )}
        </motion.div>

        {/* Warnings and Recommendations */}
        {attendanceData && attendanceData.warnings.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-4">GTU Policy Alerts</h2>
            <div className="space-y-3">
              {attendanceData.warnings.map((warning, index) => (
                <div key={index} className={`p-4 rounded-lg border-l-4 ${
                  warning.includes('SAFE') || warning.includes('✅') ? 'bg-green-50 border-green-400' :
                  warning.includes('CAUTION') || warning.includes('⚠️') ? 'bg-yellow-50 border-yellow-400' :
                  warning.includes('CRITICAL') || warning.includes('🚨') ? 'bg-red-50 border-red-400' :
                  'bg-blue-50 border-blue-400'
                }`}>
                  <p className={`font-medium ${
                    warning.includes('SAFE') || warning.includes('✅') ? 'text-green-800' :
                    warning.includes('CAUTION') || warning.includes('⚠️') ? 'text-yellow-800' :
                    warning.includes('CRITICAL') || warning.includes('🚨') ? 'text-red-800' :
                    'text-blue-800'
                  }`}>
                    {warning}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}