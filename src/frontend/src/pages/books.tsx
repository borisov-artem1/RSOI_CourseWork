import React, { useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Text from '../components/text';
import Pagination from '@mui/material/Pagination';
import GatewayService from '../services/gateway-service';
import { ThemeProvider } from '@mui/material';
import { MyTheme } from '../theme-mui';
import Alert from '@mui/material/Alert';
import settings from "../settings";
import { BookInterface, BookResponseInterface } from '../model/interface/book.interface';
import Switch from '@mui/material/Switch';
import BookCard from '../components/book-card';

interface BookPageProps {
  libraryName: string;
  libraryUuid: string;
  setValue: (value: BookInterface) => void;
}


export default function BooksPage({libraryName, libraryUuid, setValue}: BookPageProps) {
  const [books, setBooks] = useState<BookResponseInterface>();
  const [totalPages, setTotalPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [showAll, setShowAll] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string>("");

  const changePage = (_: React.ChangeEvent<unknown>, value: number) => {
    setCurrentPage(value);
  };

  const getBooks = async () => {
    const booksResponse = await GatewayService.getBooksByLibraryUuid(
      libraryUuid,
      {
        showAll: showAll,
        page: currentPage,
        size: settings.defaultPageSize,
    });

    if (booksResponse?.items
      && booksResponse?.page
      && booksResponse?.pageSize
      && booksResponse?.totalElements
    ) {
      setBooks(booksResponse);
      setTotalPages(Math.ceil(booksResponse.totalElements / booksResponse.pageSize));
      setCurrentPage(booksResponse.page);
      setErrorMsg("");
    } else {
      setBooks(undefined);
      setTotalPages(0);
      setCurrentPage(1);

      if (!booksResponse) {
        setErrorMsg("Ошибка: При запросе данных с сервиса произошла ошибка");
      } else if (!booksResponse?.totalElements) {
        setErrorMsg("Ошибка: Ничего не найдено");
      } else {
        console.log(booksResponse);
        setErrorMsg("Ошибка: Неожиданная ошибка");
      }
    }
  }

  useEffect(() => {
    getBooks();
  }, [currentPage, showAll]);

  return (
    <div className="flex flex-col p-5">
      <div className="mb-5 flex justify-center md:justify-between flex-col md:flex-row">
        <Text size="large">{libraryName}</Text>
        <div className="flex flex-row items-center">
          <ThemeProvider theme={MyTheme}>
            <Switch onChange={() => setShowAll(!showAll)} />
            <Text className="font-medium" size="little">Показать закончившиеся</Text>
          </ThemeProvider>
        </div>
      </div>

      {errorMsg &&
        <Alert
          sx={{fontWeight: 1000}}
          severity="error"
        >
          {errorMsg}
        </Alert>
      }

      <div>
        {!!totalPages &&
          <ThemeProvider theme={MyTheme}>
            <Pagination
              className="flex justify-center m-3"
              count={totalPages}
              page={currentPage}
              size="medium"
              onChange={changePage}
              color="primary" 
            />
          </ThemeProvider>
        }
      </div>

      <div className="flex flex-wrap justify-center">
        {books?.items.map(b => (
          <Card
            key={b.bookUid}
            raised={true}
            className="flex flex-col hover:bg-slate-200"
            sx={{ backgroundColor: "var(--my-third-color)", minWidth: 320, maxWidth: 320, maxHeight: 300, minHeight: 300, margin: 1.5, textWrap: "wrap"}}
          >
            <CardContent>
              <BookCard book={b} />
            </CardContent>
            <CardActions disableSpacing sx={{ mt: "auto" }}>
              <ThemeProvider theme={MyTheme}>
                <Button
                  disabled={b.availableCount === 0}
                  size="small"
                  onClick={() => setValue(b)}
                >
                  {b.availableCount === 0 ? "Закончились" : "Выбрать"}
                </Button>
              </ThemeProvider>
            </CardActions>
          </Card>
        ))}
      </div>
    </div>
  )
}
