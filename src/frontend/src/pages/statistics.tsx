import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth-service';
import Text from '../components/text';

import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import dayjs, { Dayjs } from 'dayjs';
import { Alert, Chip, ThemeProvider } from '@mui/material';
import { MyTheme } from '../theme-mui';
import { BarChart } from '@mui/x-charts/BarChart';
import { StatisticsInterface } from '../model/interface/statistics.interface';
import StatisticsService from '../services/statistics-service';
import settings from '../settings';


interface Column {
  id: "id" | "method" | "url" | "status_code" | "time";
  label: string;
  minWidth?: number;
  align?: 'right';
  format?: (value: number) => string;
}

const columns: readonly Column[] = [
  { 
    id: "id",
    label: "ID",
    minWidth: 70
  },
  {
    id: "method",
    label: "Метод",
    minWidth: 170 
  },
  {
    id: "url",
    label: "URL",
    minWidth: 300,
    // format: (value: number) => value.toLocaleString('en-US'),
  },
  {
    id: "status_code",
    label: "Код ответа",
    minWidth: 170 
  },
  {
    id: "time",
    label: "Время",
    minWidth: 170,
    align: "right",
    // format: (value: number) => value.toFixed(2),
  },
];

interface StatusCodeCounter {
  x200: number;
  x300: number;
  x400: number;
  x500: number;
}


function getChipForStatusCode (statusCode: number): JSX.Element {
  var colorForStatusCode: "success" | "warning" | "error";

  if (statusCode < 300) {
    colorForStatusCode = "success";
  } else if (statusCode < 400) {
    colorForStatusCode = "warning";
  } else {
    colorForStatusCode = "error";
  }

  return (
    <ThemeProvider theme={MyTheme}>
      <Chip className="w-full" label={statusCode} size="medium" color={colorForStatusCode} />
    </ThemeProvider>
  )
}

function countStatusCode(items: StatisticsInterface[]): StatusCodeCounter {
  const counter: StatusCodeCounter = {
    x200: 0,
    x300: 0,
    x400: 0,
    x500: 0,
  }

  for (const item of items) {
    if (item.status_code >= 200 && item.status_code < 300) {
      counter.x200 += 1;
    } else if (item.status_code >= 300 && item.status_code < 400) {
      counter.x300 += 1;
    } else if (item.status_code >= 400 && item.status_code < 500) {
      counter.x400 += 1;
    } else if (item.status_code >= 500 && item.status_code < 600) {
      counter.x500 += 1;
    }
  }

  return counter;
}


export default function StatisticsPage() {
  const navigate = useNavigate();
  const [statistics, setStatistics] = useState<StatisticsInterface[]>([]);
  const [totalElements, setTotalElements] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [rowsPerPage, setRowsPerPage] = useState(50);
  const [errorMsg, setErrorMsg] = useState<string>("");

  const [statusCodeBars, setStatusCodeBars] = useState<StatusCodeCounter>();

  const handleChangePage = (_: unknown, newPage: number) => {
    setCurrentPage(newPage+1);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setCurrentPage(1);
  };

  const getStatstics = async () => {
    const statisticsResponse = await StatisticsService.getStatistics(
      {
        page: currentPage,
        size: rowsPerPage,
    });

    if (statisticsResponse?.items
      && statisticsResponse?.page
      && statisticsResponse?.pageSize
      && statisticsResponse?.totalElements
    ) {
      setStatistics(statisticsResponse.items);
      setTotalElements(statisticsResponse.totalElements);
      setCurrentPage(statisticsResponse.page);
      setStatusCodeBars(countStatusCode(statisticsResponse.items));
      setErrorMsg("");
    } else {
      setStatistics([]);
      setCurrentPage(1);

      if (!statisticsResponse) {
        setErrorMsg("Ошибка: При запросе данных с сервиса произошла ошибка");
      } else if (!statisticsResponse?.totalElements) {
        setErrorMsg("Ошибка: Ничего не найдено");
      } else {
        console.log(statisticsResponse);
        setErrorMsg("Ошибка: Неожиданная ошибка");
      }
    }
    
  };

  useEffect(() => {
    if (!AuthService.isAdmin()) {
      navigate("/");
    }

    getStatstics();
  }, [currentPage, rowsPerPage]);

  return (
    <div
      className="p-10 mt-5 w-5/6 bg-my-third-color drop-shadow-2xl rounded-md"
    >
      <Text size="large" className="mb-5">Статистика</Text>

      {errorMsg &&
        <Alert
          sx={{fontWeight: 1000}}
          severity="error"
        >
          {errorMsg}
        </Alert>
      }

      <BarChart
        series={[
          { data: [statusCodeBars?.x200 as number], label: "2XX", color: "#008000", id: "2XXid" },
          { data: [statusCodeBars?.x300 as number], label: "3XX", color: "#DAA520", id: "3XXid" },
          { data: [statusCodeBars?.x400 as number], label: "4XX", color: "#FF0000", id: "4XXid"},
          { data: [statusCodeBars?.x500 as number], label: "5XX", color: "#8B0000", id: "5XXid" },
        ]}
        height={290}
        xAxis={[{ data: ["Статусы возврата"], scaleType: 'band', }]}
        margin={{ top: 50, bottom: 50, left: 30, right: 10 }}
      />

      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <TableContainer sx={{ maxHeight: 800 }}>
          <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell sx = {{backgroundColor: "var(--my-primary-color)", color: "var(--my-third-color)"}}
                    key={column.id}
                    align={column.align}
                    style={{ minWidth: column.minWidth }}
                  >
                    <Text size="medium">{column.label}</Text>
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {statistics
                .map((statistic) => {
                  return (
                    <TableRow hover role="checkbox" tabIndex={-1} key={statistic.id}>
                      {columns.map((column) => {
                        const value = statistic[column.id];
                        return (
                          <TableCell key={column.id} align={column.align}>
                            {column.id === "id" && <Text size="little">{value}</Text>}
                            {column.id === "method" && <Text size="little" className="underline">{value}</Text>}
                            {column.id === "url" && <Text size="little" className="font-extrabold">{value}</Text>}
                            {column.id === "status_code" && getChipForStatusCode(value as number)}
                            {column.id === "time" && <Text size="little" className="italic">{value}</Text>}
                          </TableCell>
                        );
                      })}
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[50, 100, 200]}
          component="div"
          count={totalElements}
          rowsPerPage={rowsPerPage}
          page={currentPage-1}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage={"Строк на странице"}
        />
      </Paper>
    </div>
  )
}
