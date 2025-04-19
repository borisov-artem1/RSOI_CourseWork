import React from 'react'
import { LibraryInterface } from '../model/interface/library.interface'
import { BookInterface } from '../model/interface/book.interface';
import Text from '../components/text';
import Accordion from '@mui/material/Accordion';
import AccordionActions from '@mui/material/AccordionActions';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid2';
import LibraryCard from '../components/library-card';
import BookCard from '../components/book-card';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import DateWorker from '../components/date-worker';
import { Dayjs } from 'dayjs';
import { ThemeProvider } from '@mui/material';
import { MyTheme } from '../theme-mui';

interface ReservePageProps {
  library: LibraryInterface;
  book: BookInterface;
  endDateValue: Dayjs | null;
  setEndDateValue: (value: Dayjs | null) => void;
  setAgreedValue: (value: boolean) => void;
}

export default function ReservePage({
  library,
  book,
  endDateValue,
  setEndDateValue,
  setAgreedValue,
}: ReservePageProps) {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setAgreedValue(event.target.checked);
  };

  return (
    <div className="flex flex-col p-5">
      <div className="mb-5 flex justify-center md:justify-between flex-col md:flex-row">
        <Text size="large">Подтвердите бронирование</Text>
      </div>

      <Grid container spacing={2} columns={12}>
        <Grid size={3}>
          <div>
            <Text size="medium">Выбранная</Text>
            <Text size="medium">библиотека</Text>
          </div>
        </Grid>
        <Grid size={9}>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              sx={{fontWeight: 600}}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              {library.name}
            </AccordionSummary>
            <AccordionDetails>
              <LibraryCard library={library} useName={false} />
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid size={3}>
          <div>
            <Text size="medium">Выбранная</Text>
            <Text size="medium">книга</Text>
          </div>
        </Grid>
        <Grid size={9}>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              sx={{fontWeight: 600}}
              aria-controls="panel2-content"
              id="panel2-header"
            >
              {book.name}
            </AccordionSummary>
            <AccordionDetails>
              <BookCard book={book} useName={false} />
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid size={3}>
          <div>
            <Text size="medium">Выберите дату</Text>
            <Text size="medium">возврата книги</Text>
          </div>
        </Grid>
        <Grid size={9}>
          <DateWorker
            value={endDateValue}
            setValue={(value) => {
              setEndDateValue(value);
            }}
          />
        </Grid>
      </Grid>
      
      <ThemeProvider theme={MyTheme}>
        <FormControlLabel
          className="mt-5"
          required
          control={
            <Checkbox 
              onChange={handleChange}
            />
          }
          label={
            <a href="/about/" className="hover:text-my-primary-color hover:underline">
              C правилами сайта согласен
            </a>
          }
        />
      </ThemeProvider>
    </div>
  )
}
