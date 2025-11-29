"use client"

import { useEffect, useRef } from "react"
import mermaid from "mermaid"

interface MermaidRendererProps {
  chart: string
  className?: string
}

export function MermaidRenderer({ chart, className }: MermaidRendererProps) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ref.current || !chart) return

    mermaid.initialize({
      startOnLoad: true,
      theme: "default",
      securityLevel: "loose",
    })

    const id = `mermaid-${Math.random().toString(36).slice(2, 11)}`
    ref.current.innerHTML = `<div id="${id}">${chart}</div>`

    mermaid.run({
      nodes: [ref.current.querySelector(`#${id}`)!],
    })
  }, [chart])

  return <div ref={ref} className={className} />
}

