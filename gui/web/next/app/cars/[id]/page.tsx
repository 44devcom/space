"use client"

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { useParams, useRouter } from "next/navigation"
import { fetchCar, updateCar, type Car } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { JSONEditor } from "@/components/JSONEditor"
import { MermaidRenderer } from "@/components/MermaidRenderer"
import { CarForm } from "@/components/CarForm"
import Link from "next/link"
import { ArrowLeft } from "lucide-react"

export default function CarDetailPage() {
  const params = useParams()
  const router = useRouter()
  const queryClient = useQueryClient()
  const id = params.id as string

  const { data: car, isLoading, error } = useQuery({
    queryKey: ["car", id],
    queryFn: () => fetchCar(id),
    enabled: !!id && id !== "new",
  })

  const updateMutation = useMutation({
    mutationFn: (data: Partial<Car>) => updateCar(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["car", id] })
      queryClient.invalidateQueries({ queryKey: ["cars"] })
    },
  })

  if (isLoading) {
    return (
      <div className="container mx-auto p-8">
        <p>Loading...</p>
      </div>
    )
  }

  if (error) {
    const errorMessage = error instanceof Error ? error.message : String(error)
    const isConnectionError = errorMessage.includes("Failed to fetch") || 
                              errorMessage.includes("NetworkError") ||
                              errorMessage.includes("not reachable")
    
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-8">
          <Link href="/cars">
            <Button variant="outline" className="mb-4">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Cars
            </Button>
          </Link>
          
          <Card className="border-destructive">
            <CardHeader>
              <CardTitle className="text-destructive">Error Loading Car</CardTitle>
              <CardDescription>
                {isConnectionError 
                  ? "Unable to connect to the API server"
                  : "An error occurred while loading the car"}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">
                {errorMessage}
              </p>
              
              {isConnectionError && (
                <div className="bg-muted p-4 rounded-md">
                  <p className="text-sm">
                    Please ensure the FastAPI backend is running on{" "}
                    <code className="bg-background px-1 rounded">
                      {process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}
                    </code>
                  </p>
                </div>
              )}
              
              <div className="flex gap-2">
                <Button 
                  onClick={() => queryClient.invalidateQueries({ queryKey: ["car", id] })}
                  variant="outline"
                >
                  Retry
                </Button>
                <Link href="/cars">
                  <Button variant="outline">
                    Back to Cars
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  const mermaidDiagram = car
    ? `graph TD
    A[Car ID: ${car.id}] --> B[${car.brand || "Unknown Brand"}]
    A --> C[${car.model || "Unknown Model"}]
    A --> D[${car.category || "No Category"}]
    B --> E[${car.title || "No Title"}]
    C --> E
    D --> E
    E --> F[${car.url || "No URL"}]
    style A fill:#3b82f6
    style E fill:#10b981`
    : ""

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-8">
        <Link href="/cars">
          <Button variant="outline" className="mb-4">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Cars
          </Button>
        </Link>

        <Card className="mb-6">
          <CardHeader>
            <CardTitle>{car?.title || `Car #${id}`}</CardTitle>
            <CardDescription>Car Details</CardDescription>
          </CardHeader>
        </Card>

        <Tabs defaultValue="form" className="w-full">
          <TabsList>
            <TabsTrigger value="form">Form</TabsTrigger>
            <TabsTrigger value="json">JSON</TabsTrigger>
            <TabsTrigger value="diagram">Diagram</TabsTrigger>
          </TabsList>
          <TabsContent value="form">
            <Card>
              <CardHeader>
                <CardTitle>Edit Car</CardTitle>
                <CardDescription>Update car information</CardDescription>
              </CardHeader>
              <CardContent>
                {car && (
                  <CarForm
                    initialData={car}
                    onSubmit={(data) => updateMutation.mutate(data)}
                    isSubmitting={updateMutation.isPending}
                  />
                )}
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="json">
            <Card>
              <CardHeader>
                <CardTitle>JSON View</CardTitle>
                <CardDescription>View and edit raw JSON</CardDescription>
              </CardHeader>
              <CardContent>
                <JSONEditor
                  value={JSON.stringify(car || {}, null, 2)}
                  readOnly={true}
                  height="600px"
                />
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="diagram">
            <Card>
              <CardHeader>
                <CardTitle>Visualization</CardTitle>
                <CardDescription>Mermaid diagram of car relationships</CardDescription>
              </CardHeader>
              <CardContent>
                {mermaidDiagram ? (
                  <MermaidRenderer chart={mermaidDiagram} className="w-full" />
                ) : (
                  <p className="text-muted-foreground">No data to visualize</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

