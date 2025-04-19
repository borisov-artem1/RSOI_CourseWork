import React from 'react'
import Text from '../components/text'

export default function NotFoundPage() {
  return (
    <div
      className="p-10 mt-5 w-5/6 bg-my-third-color drop-shadow-2xl rounded-md"
    >
      <div className="mb-5 flex flex-col items-center gap-10">
        <Text size="large">На этой странице ничего нет</Text>
        <Text size="high" className="font-semibold">
          <a href="/" className="hover:underline hover:text-my-primary-color">
            Перейти на главную
          </a>
        </Text>
      </div>
    </div>
  )
}
