"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Trash2, TrendingUp } from "lucide-react"

interface Car {
  id: string
  modelo: string
  marca: string
  ano: number
  cor: string
  preco: number
}

export default function VehicleDealership() {
  const [cars, setCars] = useState<Car[]>([])
  const [formData, setFormData] = useState({
    modelo: "",
    marca: "",
    ano: new Date().getFullYear(),
    cor: "",
    preco: "",
  })
  const [isLoaded, setIsLoaded] = useState(false)

  // Carregar dados do localStorage
  useEffect(() => {
    const savedCars = localStorage.getItem("vehicles")
    if (savedCars) {
      setCars(JSON.parse(savedCars))
    }
    setIsLoaded(true)
  }, [])

  // Salvar dados no localStorage
  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem("vehicles", JSON.stringify(cars))
    }
  }, [cars, isLoaded])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: name === "ano" || name === "preco" ? (value ? Number.parseFloat(value) : "") : value,
    }))
  }

  const handleAddCar = (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.modelo || !formData.marca || !formData.cor || !formData.preco) {
      alert("Por favor, preencha todos os campos")
      return
    }

    const newCar: Car = {
      id: Date.now().toString(),
      modelo: formData.modelo,
      marca: formData.marca,
      ano: formData.ano,
      cor: formData.cor,
      preco: Number(formData.preco),
    }

    setCars([...cars, newCar])
    setFormData({
      modelo: "",
      marca: "",
      ano: new Date().getFullYear(),
      cor: "",
      preco: "",
    })
  }

  const handleDeleteCar = (id: string) => {
    setCars(cars.filter((car) => car.id !== id))
  }

  const mostExpensiveCar = cars.length > 0 ? cars.reduce((max, car) => (car.preco > max.preco ? car : max)) : null

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(price)
  }

  const sortedCars = [...cars].sort((a, b) => b.preco - a.preco)

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="container mx-auto px-4 py-12 max-w-6xl">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-cyan-500 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.22.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm11 0c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z" />
              </svg>
            </div>
            <h1 className="text-4xl font-bold text-white">Gestor de Veículos</h1>
          </div>
          <p className="text-slate-400">Gerenciamento profissional de revenda de veículos</p>
        </div>

        {/* Card de Destaque - Carro Mais Caro */}
        {mostExpensiveCar && (
          <Card className="mb-8 border-0 bg-gradient-to-r from-cyan-500 to-teal-600 shadow-xl">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="w-5 h-5 text-white" />
                    <CardTitle className="text-white">Veículo Premium</CardTitle>
                  </div>
                  <CardDescription className="text-cyan-100">Maior valor em estoque</CardDescription>
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-white">{formatPrice(mostExpensiveCar.preco)}</p>
                </div>
              </div>
            </CardHeader>
            <CardContent className="text-white">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-cyan-100 text-sm">Marca</p>
                  <p className="text-lg font-semibold">{mostExpensiveCar.marca}</p>
                </div>
                <div>
                  <p className="text-cyan-100 text-sm">Modelo</p>
                  <p className="text-lg font-semibold">{mostExpensiveCar.modelo}</p>
                </div>
                <div>
                  <p className="text-cyan-100 text-sm">Ano</p>
                  <p className="text-lg font-semibold">{mostExpensiveCar.ano}</p>
                </div>
                <div>
                  <p className="text-cyan-100 text-sm">Cor</p>
                  <p className="text-lg font-semibold capitalize">{mostExpensiveCar.cor}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <div className="grid md:grid-cols-5 gap-8">
          {/* Formulário */}
          <div className="md:col-span-2">
            <Card className="border-0 bg-white shadow-lg sticky top-4">
              <CardHeader>
                <CardTitle>Adicionar Veículo</CardTitle>
                <CardDescription>Preencha os dados do novo carro</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleAddCar} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="marca">Marca</Label>
                    <Input
                      id="marca"
                      name="marca"
                      placeholder="Ex: Toyota"
                      value={formData.marca}
                      onChange={handleInputChange}
                      className="border-slate-200 focus-visible:ring-cyan-500"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="modelo">Modelo</Label>
                    <Input
                      id="modelo"
                      name="modelo"
                      placeholder="Ex: Corolla"
                      value={formData.modelo}
                      onChange={handleInputChange}
                      className="border-slate-200 focus-visible:ring-cyan-500"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="ano">Ano</Label>
                    <Input
                      id="ano"
                      name="ano"
                      type="number"
                      min="1990"
                      max={new Date().getFullYear()}
                      value={formData.ano}
                      onChange={handleInputChange}
                      className="border-slate-200 focus-visible:ring-cyan-500"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="cor">Cor</Label>
                    <Input
                      id="cor"
                      name="cor"
                      placeholder="Ex: Preto"
                      value={formData.cor}
                      onChange={handleInputChange}
                      className="border-slate-200 focus-visible:ring-cyan-500"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="preco">Preço (R$)</Label>
                    <Input
                      id="preco"
                      name="preco"
                      type="number"
                      placeholder="Ex: 65000"
                      value={formData.preco}
                      onChange={handleInputChange}
                      step="1000"
                      className="border-slate-200 focus-visible:ring-cyan-500"
                    />
                  </div>

                  <Button type="submit" className="w-full bg-cyan-500 hover:bg-cyan-600 text-white font-semibold">
                    Adicionar Veículo
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Lista de Carros */}
          <div className="md:col-span-3">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Estoque ({cars.length})</h2>
            </div>

            {cars.length === 0 ? (
              <Card className="border-0 bg-white shadow-lg">
                <CardContent className="pt-12 pb-12 text-center">
                  <p className="text-slate-500 text-lg">Nenhum veículo cadastrado ainda</p>
                  <p className="text-slate-400">Use o formulário para adicionar o primeiro carro</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {sortedCars.map((car, index) => (
                  <Card key={car.id} className="border-0 bg-white shadow-lg hover:shadow-xl transition-shadow">
                    <CardContent className="pt-6">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-3">
                            <div className="w-8 h-8 bg-cyan-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                              {index + 1}
                            </div>
                            <div>
                              <h3 className="text-lg font-bold text-slate-900">
                                {car.marca} {car.modelo}
                              </h3>
                              <p className="text-sm text-slate-500">
                                {car.ano} • {car.cor}
                              </p>
                            </div>
                          </div>
                          <div className="bg-slate-50 rounded-lg p-3 mt-3">
                            <p className="text-2xl font-bold text-cyan-600">{formatPrice(car.preco)}</p>
                          </div>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleDeleteCar(car.id)}
                          className="ml-4 text-red-500 hover:bg-red-50 hover:text-red-600"
                        >
                          <Trash2 className="w-5 h-5" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}
