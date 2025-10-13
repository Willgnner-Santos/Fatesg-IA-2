"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Trophy, Users, Database, Zap, Plus, Search } from "lucide-react"

interface Player {
  id: string
  username: string
  password: string
  xp: number
  class: string
  createdAt: string
}

const PLAYER_CLASSES = ["Warrior", "Mage", "Archer", "Rogue", "Paladin", "Necromancer"]

export default function GamePlayerManager() {
  const [players, setPlayers] = useState<Player[]>([])
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    xp: "",
    class: "",
  })
  const [searchTerm, setSearchTerm] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  // Simulate Redis-like storage using localStorage
  useEffect(() => {
    const storedPlayers = localStorage.getItem("redis-players")
    if (storedPlayers) {
      setPlayers(JSON.parse(storedPlayers))
    }
  }, [])

  const saveToStorage = (updatedPlayers: Player[]) => {
    localStorage.setItem("redis-players", JSON.stringify(updatedPlayers))
    setPlayers(updatedPlayers)
  }

  // ETL Process: Extract, Transform, Load
  const processPlayerData = (data: typeof formData): Player | null => {
    // Extract and validate
    const { username, password, xp, class: playerClass } = data

    if (!username.trim() || !password.trim() || !xp.trim() || !playerClass) {
      return null
    }

    // Transform
    const transformedData: Player = {
      id: `player:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`,
      username: username.trim().toLowerCase(),
      password: password.trim(), // In real app, this would be hashed
      xp: Math.max(0, Number.parseInt(xp) || 0),
      class: playerClass,
      createdAt: new Date().toISOString(),
    }

    return transformedData
  }

  const handleAddPlayer = async () => {
    setIsLoading(true)

    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    const processedPlayer = processPlayerData(formData)

    if (!processedPlayer) {
      alert("Please fill all fields with valid data")
      setIsLoading(false)
      return
    }

    // Check for duplicate username
    if (players.some((p) => p.username === processedPlayer.username)) {
      alert("Username already exists")
      setIsLoading(false)
      return
    }

    // Load to storage (simulating Redis SET operation)
    const updatedPlayers = [...players, processedPlayer]
    saveToStorage(updatedPlayers)

    // Reset form
    setFormData({ username: "", password: "", xp: "", class: "" })
    setIsLoading(false)
  }

  // Simulate Redis ZRANGE for ranking (sorted by XP)
  const getTopPlayers = () => {
    return [...players].sort((a, b) => b.xp - a.xp).slice(0, 10)
  }

  const filteredPlayers = players.filter(
    (player) =>
      player.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      player.class.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const stats = {
    totalPlayers: players.length,
    totalXP: players.reduce((sum, p) => sum + p.xp, 0),
    avgXP: players.length > 0 ? Math.round(players.reduce((sum, p) => sum + p.xp, 0) / players.length) : 0,
    topClass:
      players.length > 0
        ? Object.entries(
            players.reduce(
              (acc, p) => {
                acc[p.class] = (acc[p.class] || 0) + 1
                return acc
              },
              {} as Record<string, number>,
            ),
          ).sort(([, a], [, b]) => b - a)[0]?.[0] || "None"
        : "None",
  }

  return (
    <div className="container mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-balance">Gaming Player Manager</h1>
        <p className="text-xl text-muted-foreground text-pretty">
          Advanced player management system with XP tracking, ETL processing, and Redis-like functionality
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Players</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">{stats.totalPlayers}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total XP</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-accent">{stats.totalXP.toLocaleString()}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average XP</CardTitle>
            <Database className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-chart-2">{stats.avgXP}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Top Class</CardTitle>
            <Trophy className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-chart-3">{stats.topClass}</div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="add-player" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="add-player">Add Player</TabsTrigger>
          <TabsTrigger value="rankings">XP Rankings</TabsTrigger>
          <TabsTrigger value="all-players">All Players</TabsTrigger>
        </TabsList>

        {/* Add Player Tab */}
        <TabsContent value="add-player">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Plus className="h-5 w-5" />
                Add New Player
              </CardTitle>
              <CardDescription>
                ETL Process: Data will be extracted, transformed, and loaded into the Redis-like storage
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="username">Username</Label>
                  <Input
                    id="username"
                    placeholder="Enter username"
                    value={formData.username}
                    onChange={(e) => setFormData((prev) => ({ ...prev, username: e.target.value }))}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Enter password"
                    value={formData.password}
                    onChange={(e) => setFormData((prev) => ({ ...prev, password: e.target.value }))}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="xp">Experience Points</Label>
                  <Input
                    id="xp"
                    type="number"
                    placeholder="Enter XP"
                    value={formData.xp}
                    onChange={(e) => setFormData((prev) => ({ ...prev, xp: e.target.value }))}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="class">Class</Label>
                  <Select
                    value={formData.class}
                    onValueChange={(value) => setFormData((prev) => ({ ...prev, class: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select class" />
                    </SelectTrigger>
                    <SelectContent>
                      {PLAYER_CLASSES.map((cls) => (
                        <SelectItem key={cls} value={cls}>
                          {cls}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button onClick={handleAddPlayer} disabled={isLoading} className="w-full">
                {isLoading ? "Processing..." : "Add Player"}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Rankings Tab */}
        <TabsContent value="rankings">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Trophy className="h-5 w-5" />
                XP Rankings
              </CardTitle>
              <CardDescription>Top 10 players sorted by experience points (Redis ZRANGE simulation)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {getTopPlayers().map((player, index) => (
                  <div key={player.id} className="flex items-center justify-between p-4 rounded-lg border bg-card">
                    <div className="flex items-center gap-4">
                      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold">
                        {index + 1}
                      </div>
                      <div>
                        <p className="font-semibold">{player.username}</p>
                        <p className="text-sm text-muted-foreground">{player.class}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-accent">{player.xp.toLocaleString()}</p>
                      <p className="text-sm text-muted-foreground">XP</p>
                    </div>
                  </div>
                ))}
                {players.length === 0 && <p className="text-center text-muted-foreground py-8">No players added yet</p>}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* All Players Tab */}
        <TabsContent value="all-players">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                All Players
              </CardTitle>
              <CardDescription>Browse and search all players in the database</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-2">
                <Search className="h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search by username or class..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="flex-1"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredPlayers.map((player) => (
                  <Card key={player.id}>
                    <CardContent className="p-4">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold">{player.username}</h3>
                          <Badge variant="secondary">{player.class}</Badge>
                        </div>
                        <p className="text-2xl font-bold text-accent">{player.xp.toLocaleString()} XP</p>
                        <p className="text-xs text-muted-foreground">
                          Added: {new Date(player.createdAt).toLocaleDateString()}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {filteredPlayers.length === 0 && players.length > 0 && (
                <p className="text-center text-muted-foreground py-8">No players match your search</p>
              )}
              {players.length === 0 && <p className="text-center text-muted-foreground py-8">No players added yet</p>}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
