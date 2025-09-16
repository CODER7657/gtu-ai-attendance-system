'use client'
import { motion } from 'framer-motion'
import { AcademicCapIcon, ChartBarIcon, CalendarIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'

export default function Navbar() {
  return (
    <motion.nav 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="bg-white shadow-lg border-b border-gray-200"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <AcademicCapIcon className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">AI Attendance</span>
          </div>
          
          {/* Navigation Links */}
          <div className="hidden md:flex space-x-8">
            <NavLink href="/dashboard" icon={ChartBarIcon} text="Dashboard" />
            <NavLink href="/calendar" icon={CalendarIcon} text="Calendar" />
            <NavLink href="/upload" icon={AcademicCapIcon} text="Upload" />
            <NavLink href="/chat" icon={ChatBubbleLeftRightIcon} text="AI Chat" />
          </div>
        </div>
      </div>
    </motion.nav>
  )
}

function NavLink({ href, icon: Icon, text }: { 
  href: string, 
  icon: any, 
  text: string 
}) {
  return (
    <a 
      href={href}
      className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition-colors"
    >
      <Icon className="h-5 w-5" />
      <span>{text}</span>
    </a>
  )
}