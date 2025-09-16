'use client'
import Navbar from '@/components/layout/Navbar'
import GTUDashboard from '@/components/dashboard/GTUDashboard'

export default function DashboardPage() {
  return (
    <>
      <Navbar />
      <main>
        <GTUDashboard />
      </main>
    </>
  )
}