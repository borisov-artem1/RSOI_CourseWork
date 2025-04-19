import React, { useCallback, useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Text from '../components/text';
import Pagination from '@mui/material/Pagination';
import { LibraryInterface, LibraryResponseInterface } from '../model/interface/library.interface';
import GatewayService from '../services/gateway-service';
import InputField from '../components/input-field';
import { ThemeProvider } from '@mui/material';
import { MyTheme } from '../theme-mui';
import Alert from '@mui/material/Alert';
import settings from "../settings";
import LibraryCard from '../components/library-card';

interface LibraryPageProps {
  setValue: (value: LibraryInterface) => void;
}


export default function LibrariesPage({setValue}: LibraryPageProps) {
  const [libraries, setLibraries] = useState<LibraryResponseInterface>();
  const [totalPages, setTotalPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [city, setCity] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string>("");

  const changePage = (_: React.ChangeEvent<unknown>, value: number) => {
    setCurrentPage(value);
  };

  const getLibraries = async () => {
    // const librariesResponse = await LibraryService.getLibraries(); // library_uid
    const librariesResponse = await GatewayService.getLibraries({
      city: city,
      page: currentPage,
      size: settings.defaultPageSize,
    });

    if (librariesResponse?.items
      && librariesResponse?.page
      && librariesResponse?.pageSize
      && librariesResponse?.totalElements
    ) {
      setLibraries(librariesResponse);
      setTotalPages(Math.ceil(librariesResponse.totalElements / librariesResponse.pageSize));
      setCurrentPage(librariesResponse.page);
      setErrorMsg("");
    } else {
      setLibraries(undefined);
      setTotalPages(0);
      setCurrentPage(1);

      if (!librariesResponse) {
        setErrorMsg("Ошибка: При запросе данных с сервиса произошла ошибка");
      } else if (!librariesResponse?.totalElements) {
        setErrorMsg("Ошибка: Ничего не найдено");
      } else {
        console.log(librariesResponse);
        setErrorMsg("Ошибка: Неожиданная ошибка");
      }
    }
  }

  useEffect(() => {
    getLibraries();
  }, [currentPage]);

  return (
    <div className="flex flex-col p-5">
      <div className="mb-5 flex justify-between flex-col md:flex-row">
        <Text size="large">Все библиотеки</Text>
        <div className="flex flex-col md:flex-row gap-5">
          <InputField label="Город" value={city} setValue={(value: string) => {
            setCity(value);
          }}/>
          <ThemeProvider theme={MyTheme}>
            <Button
              sx={{
                fontSize: "var(--my-little-size)"
              }}
              color="secondary"
              size="small"
              variant="outlined"
              onClick={ getLibraries }
            >
              Искать
            </Button>
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
              color="primary" />
          </ThemeProvider>
        }
      </div>

      <div className="flex flex-wrap justify-center">
        {libraries?.items.map(l => (
          <Card
            key={l.libraryUid}
            raised={true}
            className="flex flex-col hover:bg-slate-200"
            sx={{ backgroundColor: "var(--my-third-color)", minWidth: 320, maxWidth: 320, maxHeight: 300, minHeight: 300, margin: 1.5, textWrap: "wrap"}}
          >
          <CardContent>
            <LibraryCard library={l} />
          </CardContent>
          <CardActions disableSpacing sx={{ mt: "auto" }}>
            <ThemeProvider theme={MyTheme}>
              <Button
                size="small"
                onClick={() => setValue(l)}
              >
                Смотреть книги
              </Button>
            </ThemeProvider>
          </CardActions>
        </Card>
        ))}
      </div>
    </div>
  )
}
