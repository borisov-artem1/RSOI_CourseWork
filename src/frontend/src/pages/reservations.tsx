import React, { useEffect, useState } from 'react'
import Text from '../components/text'

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import { Chip, ThemeProvider } from '@mui/material';
import GatewayService from '../services/gateway-service';
import settings from '../settings';

import Accordion from '@mui/material/Accordion';
import AccordionActions from '@mui/material/AccordionActions';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Grid from '@mui/material/Grid2';
import { ReservationInterface, ReservationStatusType } from '../model/interface/reservation.interface';
import { MyTheme } from '../theme-mui';
import LibraryCard from '../components/library-card';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import BookCard from '../components/book-card';
import Alert from '@mui/material/Alert';
import Pagination from '@mui/material/Pagination';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import dayjs from 'dayjs';

import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import { BookConditionType } from '../model/interface/book.interface';
import { useNavigate } from 'react-router-dom';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import AuthService from '../services/auth-service';

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'var(--my-third-color)',
  // border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};



function createData(
  name: string,
  calories: number,
  fat: number,
  carbs: number,
  protein: number,
) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
  createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
  createData('Eclair', 262, 16.0, 24, 6.0),
  createData('Cupcake', 305, 3.7, 67, 4.3),
  createData('Gingerbread', 356, 16.0, 49, 3.9),
];


function getChipForReservationStatus (status: ReservationStatusType): JSX.Element {
  var statusTranslated;
  var colorForStatus: "primary" | "error" | "success";

  if (status === "RENTED") {
    statusTranslated = "В АРЕНДЕ";
    colorForStatus = "primary";
  } else if (status === "EXPIRED") {
    statusTranslated = "СДАНА ПОСЛЕ СРОКА";
    colorForStatus = "error";
  } else {
    statusTranslated = "СДАНА В СРОК";
    colorForStatus = "success";
  }

  return (
    <ThemeProvider theme={MyTheme}>
      <Chip className="w-full m-5" label={statusTranslated} size="medium" color={colorForStatus} />
    </ThemeProvider>
  )
}

export default function ReservationsPage() {
  const [reservations, setReservations] = useState<ReservationInterface[]>();
  const [totalPages, setTotalPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [reservationStatus, setReservationStatus] = useState<ReservationStatusType>("");
  const [chosenReservationUuid, setChosenReservationUuid] = useState<string>();
  const [bookCondition, setBookCondition] = useState<BookConditionType>("EXCELLENT");
  const [open, setOpen] = React.useState(false);
  const [agreed, setAgreed] = React.useState(false);
  const [errorMsg, setErrorMsg] = useState<string>("");
  const [errorModalMsg, setErrorModalMsg] = useState<string>("");
  const navigate = useNavigate();

  const [expandAccordions, setExpandAccordions] = useState<number[]>([]);

  const handleClose = () => {
    setOpen(false);
  };

  const accordionClicked = (index: number) => {
    if (expandAccordions.includes(index)) {
      setExpandAccordions(
        expandAccordions.filter((number) => number !== index)
      );
    }
    else {
      setExpandAccordions([...expandAccordions, index]);
    }
  }

  const collapseAll = () => {
    setExpandAccordions([]);
  }

  const handleOpen = (reservationUuid: string) => {
    setErrorModalMsg("");
    setChosenReservationUuid(reservationUuid);
    setBookCondition("EXCELLENT");
    setOpen(true);
  };

  const getReservations = async () => {
    const reservationResponse = await GatewayService.getUserReservations(
    {
      status: reservationStatus === "" ? undefined : reservationStatus,
      page: currentPage,
      size: settings.defaultPageSize,
    });

    if (reservationResponse?.items
      && reservationResponse?.page
      && reservationResponse?.pageSize
      && reservationResponse?.totalElements
    ) {
      setReservations(reservationResponse.items);
      setTotalPages(Math.ceil(reservationResponse.totalElements / reservationResponse.pageSize));
      setCurrentPage(reservationResponse.page);
      setErrorMsg("");
    } else {
      setReservations(undefined);
      setTotalPages(0);
      setCurrentPage(1);

      if (!reservationResponse) {
        setErrorMsg("Ошибка: При запросе данных с сервиса произошла ошибка");
      } else if (!reservationResponse?.totalElements) {
        setErrorMsg("Ошибка: Ничего не найдено");
      } else {
        console.log(reservationResponse);
        setErrorMsg("Ошибка: Неожиданная ошибка");
      }
    }
  }

  const handleReservationStatus = (event: SelectChangeEvent) => {
    const status = event.target.value;

    if (status === "RENTED") {
      setReservationStatus("RENTED");
    } else if (status === "EXPIRED") {
      setReservationStatus("EXPIRED");
    } else if (status === "RETURNED") {
      setReservationStatus("RETURNED");
    } else if (status === "") {
      setReservationStatus("");
    }else {
      setErrorMsg("Ошибка: Неожиданный тип статуса бронирования");
    }
  }

  const handleBookCondition = (event: SelectChangeEvent) => {
    const condition = event.target.value;

    if (condition === "EXCELLENT") {
      setBookCondition("EXCELLENT");
    } else if (condition === "GOOD") {
      setBookCondition("GOOD");
    } else if (condition === "BAD") {
      setBookCondition("BAD");
    } else if (condition === "") {
      setBookCondition("");
    } else {
      setErrorMsg("Ошибка: Неожиданный тип состояния книги");
    }

    
  }

  const changePage = (_: React.ChangeEvent<unknown>, value: number) => {
    setCurrentPage(value);
  };

  const handleCheckbox = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAgreed(event.target.checked);
  };

  const handleReturnBook = async () => {
    if (chosenReservationUuid && bookCondition && agreed) {
      const now = dayjs();

      const response = await GatewayService.returnBook({
        reservationUuid: chosenReservationUuid,
        condition: bookCondition,
        date: now,
      });

      if (typeof response === "string") {
        setErrorModalMsg(response);
      } else {
        handleClose();
        collapseAll();
      }
    } else {
      setErrorModalMsg("Ошибка: не все данные заполнены");
    }

    await getReservations();
  }

  useEffect(() => {
    if (!AuthService.isAuth()) {
      navigate("/");
    }
    
    getReservations();
  }, [currentPage, reservationStatus]);

  return (
    <div
      className="flex flex-col p-10 mt-5 w-5/6 bg-my-third-color drop-shadow-2xl rounded-md"
    >
      <div className="mb-5 flex justify-center md:justify-between flex-col md:flex-row">
        <Text size="large" className="mb-5">Бронирования</Text>
        <ThemeProvider theme={MyTheme}>
          <FormControl className="md:w-3/12 w-full" sx={{minWidth: "250px"}}>
            <InputLabel id="demo-simple-select-label">Статус бронирования</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={reservationStatus}
              label="Статус бронирования"
              onChange={handleReservationStatus}
            >
              <MenuItem value={""}><em>Все</em></MenuItem>
              <MenuItem value={"RENTED"}>В аренде</MenuItem>
              <MenuItem value={"RETURNED"}>Сдана в срок</MenuItem>
              <MenuItem value={"EXPIRED"}>Сдана после срока</MenuItem>
            </Select>
          </FormControl>
        </ThemeProvider>
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

      <Grid container spacing={2} columns={12}>
        {reservations?.map((r, index) => (
          <React.Fragment key={index}>
            <Grid size={10}>
              <Accordion
                expanded={expandAccordions.includes(index)}
                onChange={() => accordionClicked(index)}
              >
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  sx={{fontWeight: 600}}
                  aria-controls="panel1-content"
                  id="panel1-header"
                >
                  <div className="flex flex-col">
                    <div className="flex row gap-3">
                      <Text className="min-w-32" size="medium">Книга:</Text>
                      <Text size="medium">{r.book.name}</Text>
                    </div>
                    <div className="flex row gap-3">
                      <Text className="min-w-32" size="medium">Библиотека:</Text>
                      <Text size="medium">{r.library.name}</Text>
                    </div>
                  </div>
                </AccordionSummary>
                <AccordionDetails>
                <div className="flex flex-wrap justify-center gap-8 mx-5">
                  <Card
                    key="library"
                    raised={true}
                    className="mt-5 flex flex-auto justify-center max-w-screen-sm"
                    sx={{ backgroundColor: "var(--my-third-color)", textWrap: "wrap" }}
                  >
                    <CardContent>
                      <Text className="font-extrabold" size="medium">Библиотека</Text>
                      <Divider className="" />
                      <LibraryCard className="mt-3" library={r.library} useName={false} />
                    </CardContent>
                  </Card>

                  <Card
                    key="book"
                    raised={true}
                    className="mt-5 flex flex-auto justify-center max-w-screen-sm"
                    sx={{ backgroundColor: "var(--my-third-color)", textWrap: "wrap" }}
                  >
                    <CardContent>
                      <Text className="font-extrabold" size="medium">Книга</Text>
                      <Divider />
                      <BookCard className="mt-3" book={r.book} useName={false} useCount={false} />
                    </CardContent>
                  </Card>

                  <Card
                    key="reservation"
                    raised={true}
                    className="mt-5 flex flex-auto justify-center max-w-screen-sm"
                    sx={{ backgroundColor: "var(--my-third-color)", textWrap: "wrap"} }
                  >
                    <CardContent>
                      <Text className="font-extrabold" size="medium">Даты бронирования</Text>
                      <Divider />
                      <div className="flex flex-row gap-2 mt-3">
                        <Text size="little" className="font-semibold min-w-24">Взята:</Text>
                        <Text size="little">{r.startDate}</Text>
                      </div>
                      <div className="flex flex-row gap-2">
                        <Text size="little" className="font-semibold min-w-24">Вернуть до:</Text>
                        <Text size="little">{r.tillDate}</Text>
                      </div>
                    </CardContent>
                  </Card>
                </div>
                </AccordionDetails>
                {r.status === "RENTED" &&
                  <AccordionActions className="mb-3 mr-3">
                    <ThemeProvider theme={MyTheme}>
                      <Button
                        variant="outlined"
                        size="large"
                        onClick={() => {
                          handleOpen(r.reservationUid);
                        }}
                      >
                        ВЕРНУТЬ КНИГУ
                      </Button>
                    </ThemeProvider>
                  </AccordionActions>
                }
              </Accordion>
            </Grid>
            <Grid size={2}>
              {getChipForReservationStatus(r.status)}
            </Grid>
          </React.Fragment>
        ))}
      </Grid>
      
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} className="flex flex-col gap-7">
          <Text size="high">Вернуть книгу</Text>

          <ThemeProvider theme={MyTheme}>
            <FormControl>
              <InputLabel id="demo-simple-select-label">Состояние книги</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={bookCondition}
                label="Состояние книги"
                onChange={handleBookCondition}
                defaultValue="EXCELLENT"
              >
                <MenuItem value={"EXCELLENT"}>Прекрасное</MenuItem>
                <MenuItem value={"GOOD"}>Хорошее</MenuItem>
                <MenuItem value={"BAD"}>Плохое</MenuItem>
              </Select>
            </FormControl>

            <FormControlLabel
              className="mt-5"
              required
              control={
                <Checkbox 
                  onChange={handleCheckbox}
                />
              }
              label={
                <a href="/about/" className="hover:text-my-primary-color hover:underline">
                  C правилами сайта согласен
                </a>
              }
            />

            {errorModalMsg &&
              <Alert
                sx={{fontWeight: 1000}}
                severity="error"
              >
                {errorMsg}
              </Alert>
            }

            <div className="flex flex-col gap-3">
              <Button
                disabled={!agreed}
                variant="contained"
                size="large"
                onClick={async () => await handleReturnBook()}
              >
                ПОДТВЕРДИТЬ
              </Button>

              <Button
                variant="contained"
                size="large"
                onClick={handleClose}
              >
                ОТМЕНИТЬ
              </Button>
            </div>
          </ThemeProvider>
        </Box>
      </Modal>

    </div>
  )
}
