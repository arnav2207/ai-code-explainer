import Link from "next/link";
import { ArrowRight, Braces, Gauge, GraduationCap, ShieldCheck } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const features = [
  {
    title: "Structured Explanations",
    description: "Get summaries, line-by-line walkthroughs, complexity, variables, and improvements.",
    icon: Braces,
  },
  {
    title: "Beginner Friendly",
    description: "Translate unfamiliar syntax and control flow into practical language.",
    icon: GraduationCap,
  },
  {
    title: "Built For Flow",
    description: "Paste code, choose a language, and get an answer without leaving the editor.",
    icon: Gauge,
  },
  {
    title: "Production Shape",
    description: "Typed API contracts, clear error states, and a clean UI ready to extend.",
    icon: ShieldCheck,
  },
];

export default function HomePage() {
  return (
    <main>
      <section className="container grid min-h-[calc(100vh-4rem)] items-center gap-10 py-12 lg:grid-cols-[1fr_0.86fr] lg:py-16">
        <div className="max-w-3xl">
          <p className="mb-4 inline-flex rounded-md border bg-card px-3 py-1 text-sm font-medium text-muted-foreground">
            Gemini-powered code understanding
          </p>
          <h1 className="text-balance text-4xl font-semibold tracking-normal text-foreground sm:text-5xl lg:text-6xl">
            AI Code Explainer
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">
            Paste unfamiliar code and get a clear, structured explanation designed for learning,
            debugging, and faster onboarding.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button asChild size="lg">
              <Link href="/explainer">
                Open Explainer
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <a href="#features">View Features</a>
            </Button>
          </div>
        </div>

        <div className="rounded-lg border bg-slate-950 p-4 shadow-soft">
          <div className="mb-3 flex items-center gap-2">
            <span className="h-3 w-3 rounded-full bg-red-400" />
            <span className="h-3 w-3 rounded-full bg-amber-300" />
            <span className="h-3 w-3 rounded-full bg-emerald-400" />
          </div>
          <pre className="overflow-hidden rounded-md bg-slate-900 p-5 text-sm leading-7 text-slate-100">
            <code>{`def greet(name):
    message = f"Hello, {name}"
    return message

print(greet("Ada"))`}</code>
          </pre>
          <div className="mt-4 rounded-md border border-teal-300/25 bg-teal-300/10 p-4 text-sm leading-6 text-teal-50">
            <p className="font-medium text-teal-100">Summary</p>
            <p className="mt-1 text-teal-50/85">
              Defines a small function, stores a greeting in a variable, returns it, then prints
              the result.
            </p>
          </div>
        </div>
      </section>

      <section id="features" className="border-t bg-white/70 py-14">
        <div className="container">
          <div className="mb-8 max-w-2xl">
            <h2 className="text-2xl font-semibold">Designed For Code Reading</h2>
            <p className="mt-2 text-muted-foreground">
              A focused interface for understanding code quickly, with enough structure to be useful
              beyond a one-line answer.
            </p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <Card key={feature.title} className="bg-card/90">
                <CardHeader>
                  <feature.icon className="h-5 w-5 text-primary" />
                  <CardTitle className="pt-2 text-base">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm leading-6 text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
