import React from "react";
import { CheckCircleIcon } from "@heroicons/react/24/outline";

export default function Landing() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Your SaaS Platform for Modern Business
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Streamline your operations, enhance productivity, and drive growth
              with our comprehensive solution.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <a
                href="/dashboard"
                className="rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
              >
                Get started
              </a>
              <a
                href="/learn-more"
                className="text-sm font-semibold leading-6 text-gray-900"
              >
                Learn more <span aria-hidden="true">→</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-24 sm:py-32">
        {/* ... rest of the landing page code ... */}
      </div>
    </div>
  );
}
