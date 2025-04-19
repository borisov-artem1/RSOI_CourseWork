import React from 'react'
import Text from './text';
import { BookConditionType, BookInterface } from '../model/interface/book.interface';

interface BookCardProps {
  useName?: boolean;
  useCount?: boolean;
  useCondition?: boolean;
  book: BookInterface;
  className?: string;
}

function translateCondition(condition: BookConditionType): string {
  const translator: Record<string, string> = {
    "EXCELLENT": "Прекрасное",
    "GOOD": "Хорошее", 
    "BAD": "Плохое",
  }

  return translator[condition];
}

export default function BookCard({
  book,
  className,
  useName = true,
  useCondition = true,
  useCount = true,
}: BookCardProps) {
  return (
    <div className={className}>
      {useName && 
        <React.Fragment>
          <Text size="medium" className="font-extrabold">{book.name}</Text>
          <br />
        </React.Fragment>
      }
      <div className="flex flex-row gap-2">
        <Text size="little" className="font-semibold min-w-24">Автор:</Text>
        <Text size="little">{book.author}</Text>
      </div>
      <div className="flex flex-row gap-2">
        <Text size="little" className="font-semibold min-w-24">Жанр:</Text>
        <Text size="little">{book.genre}</Text>
      </div>
      {useCondition &&
        <div className="flex flex-row gap-2">
          <Text size="little" className="font-semibold min-w-24">Состояние:</Text>
          <Text size="little">{translateCondition(book.condition)}</Text>
        </div>
      }
      

      {useCount &&
        <React.Fragment>
          <br />
          <div className="flex flex-row gap-2">
            <Text size="little" className="font-semibold min-w-14">Количество:</Text>
            <Text size="little">{book.availableCount}</Text>
          </div>
        </React.Fragment>
      }
    </div>
  )
}
