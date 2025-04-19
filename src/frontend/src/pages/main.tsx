import LibrariesPage from "./libraries";
import * as React from 'react';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import BooksPage from "./books";
import { ThemeProvider } from "@mui/material";
import { MyTheme } from "../theme-mui";
import { LibraryInterface } from "../model/interface/library.interface";
import { BookInterface } from "../model/interface/book.interface";
import ReservePage from "./reserve";
import Text from "../components/text";
import AuthService from "../services/auth-service";
import Alert from '@mui/material/Alert';
import { Dayjs } from "dayjs";
import GatewayService from "../services/gateway-service";
import { useNavigate } from 'react-router-dom';

const steps = ['Выберите библиотеку', 'Выберите книгу', 'Забронируйте книгу'];


export default function MainPage() {
  const [activeStep, setActiveStep] = React.useState(0);
  const [chosenLibrary, setChosenLibrary] = React.useState<LibraryInterface>();
  const [chosenBook, setChosenBook] = React.useState<BookInterface>();
  const [chosenEndTime, setChosenEndTime] = React.useState<Dayjs | null>(null);
  const [agreed, setAgreed] = React.useState<boolean>(false);
  const [errorMsg, setErrorMsg] = React.useState<string>("");
  const navigate = useNavigate();


  const handleReserve = async () => {
    if (AuthService.isAuth() && agreed && chosenEndTime) {
      const response = await GatewayService.reserveBook({
        libraryUuid: chosenLibrary?.libraryUid as string,
        booUuid: chosenBook?.bookUid as string,
        tillDate: chosenEndTime,
      });

      if (typeof response === "string") {
        setErrorMsg(response);
      } else {
        handleNext();
      }
    } else {
      setErrorMsg("Ошибка: Чтобы забронировать книгу, нужно авторизоваться");
    }
  }

  const handleNext = () => {
    setErrorMsg("");
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setErrorMsg("");
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  const goToReservationsPage = () => {
    navigate(`/reservations`)
  };

  return (
    <div
      className="p-10 mt-5 w-5/6 bg-my-third-color drop-shadow-2xl rounded-md"
    >
      <Box sx={{ width: '100%' }} className="flex flex-col justify-center items-stretch">
        <Stepper activeStep={activeStep}>
          {steps.map((label, _) => {
            const stepProps: { completed?: boolean } = {};
            const labelProps: {
              optional?: React.ReactNode;
            } = {};
            return (
              <Step key={label} {...stepProps}>
                <ThemeProvider theme={MyTheme}>
                  <StepLabel {...labelProps}>{label}</StepLabel>
                </ThemeProvider>
              </Step>
            );
          })}
        </Stepper>
        {activeStep === steps.length ? (
          <React.Fragment>
            <div className="flex flex-col p-5 gap-5">
              <Text
                size="large"
              >
                Книга успешно забронирована
              </Text>
              <ThemeProvider theme={MyTheme}>
                <div
                  className="flex flex-col justify-center gap-5 items-center"
                >
                  <Button
                    color="primary"
                    size="large"
                    variant="outlined"
                    onClick={goToReservationsPage}
                  >
                    Посмотреть мои бронирования
                  </Button>
                  <Button 
                    color="primary"
                    size="large"
                    variant="outlined"
                    onClick={handleReset}
                  >
                    Забронировать еще
                  </Button>
                </div>
              </ThemeProvider>
            </div>
          </React.Fragment>
        ) : (
          <React.Fragment>
            {/* <Typography sx={{ mt: 2, mb: 1 }}>Шаг {activeStep + 1}</Typography> */}

            {activeStep === 0 && <LibrariesPage setValue={(value: LibraryInterface) => {
              handleNext();
              setChosenLibrary(value);
            }}/>}

            {activeStep === 1 && <BooksPage
              libraryName={(chosenLibrary as LibraryInterface).name}
              libraryUuid={(chosenLibrary as LibraryInterface).libraryUid}
              setValue={(value: BookInterface) => {
                handleNext();
                setChosenBook(value);
              }
            }/>}

            {activeStep === 2 &&
              <ReservePage
                library={(chosenLibrary as LibraryInterface)}
                book={(chosenBook as BookInterface)}
                endDateValue={chosenEndTime}
                setEndDateValue={(value: Dayjs | null) => {
                  setChosenEndTime(value);
                }}
                setAgreedValue={(value: boolean) => {
                  setAgreed(value);
                }}
              />}

            {errorMsg &&
              <Alert
                sx={{fontWeight: 1000}}
                severity="error"
              >
                {errorMsg}
              </Alert>
            }

            <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
              <Button
                color="inherit"
                disabled={activeStep === 0}
                onClick={handleBack}
                sx={{ mr: 1 }}
              >
                Назад
              </Button>
              <Box sx={{ flex: '1 1 auto' }} />
              {activeStep === 2 &&
                <ThemeProvider theme={MyTheme}>
                  <Button
                    disabled={!agreed || chosenEndTime === null}
                    color="primary"
                    size="large"
                    variant="outlined"
                    onClick={handleReserve}
                  >
                    Забронировать
                  </Button>
                </ThemeProvider>
              }
            </Box>
          </React.Fragment>
        )}
      </Box>
    </div>
    
  );
}
