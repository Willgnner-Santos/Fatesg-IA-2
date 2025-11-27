"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { StatsCards } from "@/components/stats-cards"
import { WorkoutTimeline } from "@/components/workout-timeline"
import { WeeklyCalendar } from "@/components/weekly-calendar"
import { AddWorkoutModal } from "@/components/add-workout-modal"
import { WorkoutFilters } from "@/components/workout-filters"
import type { Workout } from "@/types/workout"

// Dados iniciais de exemplo
const initialWorkouts: Workout[] = [
  {
    id: "1",
    date: "2025-01-20",
    title: "Treino de Peito e Tríceps",
    description: "Supino reto, supino inclinado, crucifixo, tríceps pulley e mergulho",
    status: "completed",
    tags: ["strength", "upper-body"],
    duration: 90,
  },
  {
    id: "2",
    date: "2025-01-22",
    title: "Cardio Intervalado HIIT",
    description: "30 minutos de treino intervalado de alta intensidade na esteira",
    status: "completed",
    tags: ["cardio", "hiit"],
    duration: 30,
  },
  {
    id: "3",
    date: "2025-01-23",
    title: "Treino de Costas e Bíceps",
    description: "Barra fixa, remada curvada, pulldown, rosca direta e rosca martelo",
    status: "in-progress",
    tags: ["strength", "upper-body"],
    duration: 85,
  },
  {
    id: "4",
    date: "2025-01-25",
    title: "Yoga e Alongamento",
    description: "Sessão de yoga focada em flexibilidade e recuperação muscular",
    status: "pending",
    tags: ["flexibility", "recovery"],
    duration: 60,
  },
  {
    id: "5",
    date: "2025-01-26",
    title: "Treino de Pernas Completo",
    description: "Agachamento livre, leg press, cadeira extensora, cadeira flexora e panturrilha",
    status: "pending",
    tags: ["strength", "lower-body"],
    duration: 100,
  },
  {
    id: "6",
    date: "2025-01-27",
    title: "Spinning Class",
    description: "Aula de spinning de 45 minutos com foco em resistência",
    status: "pending",
    tags: ["cardio", "endurance"],
    duration: 45,
  },
  {
    id: "7",
    date: "2025-01-28",
    title: "Treino de Ombros e Abdômen",
    description: "Desenvolvimento militar, elevação lateral, remada alta e abdominais variados",
    status: "pending",
    tags: ["strength", "core"],
    duration: 70,
  },
]

export default function Home() {
  const [workouts, setWorkouts] = useState<Workout[]>(initialWorkouts)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedDate, setSelectedDate] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState<string>("all")
  const [tagFilter, setTagFilter] = useState<string>("all")

  const addWorkout = (workout: Omit<Workout, "id">) => {
    const newWorkout: Workout = {
      ...workout,
      id: Date.now().toString(),
    }
    setWorkouts([...workouts, newWorkout].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()))
  }

  const deleteWorkout = (id: string) => {
    setWorkouts(workouts.filter((w) => w.id !== id))
  }

  const updateWorkout = (id: string, updates: Partial<Workout>) => {
    setWorkouts(workouts.map((w) => (w.id === id ? { ...w, ...updates } : w)))
  }

  // Filtrar workouts
  const filteredWorkouts = workouts.filter((workout) => {
    const matchesSearch =
      workout.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      workout.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || workout.status === statusFilter
    const matchesTag = tagFilter === "all" || workout.tags.includes(tagFilter)
    const matchesDate = !selectedDate || workout.date === selectedDate

    return matchesSearch && matchesStatus && matchesTag && matchesDate
  })

  return (
    <div className="min-h-screen bg-background">
      <Header onAddWorkout={() => setIsModalOpen(true)} />

      <main className="container mx-auto px-4 py-8 max-w-7xl">
        <StatsCards workouts={workouts} />

        <div className="grid lg:grid-cols-[1fr_300px] gap-6 mt-8">
          <div className="space-y-6">
            <WorkoutFilters
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
              statusFilter={statusFilter}
              onStatusFilterChange={setStatusFilter}
              tagFilter={tagFilter}
              onTagFilterChange={setTagFilter}
            />

            <WorkoutTimeline workouts={filteredWorkouts} onDelete={deleteWorkout} onUpdateStatus={updateWorkout} />
          </div>

          <div>
            <WeeklyCalendar workouts={workouts} selectedDate={selectedDate} onDateSelect={setSelectedDate} />
          </div>
        </div>
      </main>

      <AddWorkoutModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onAdd={addWorkout} />
    </div>
  )
}
