import React from 'react'
import Text from '../components/text'
import Accordion from '@mui/material/Accordion';
import AccordionActions from '@mui/material/AccordionActions';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MultilineText from '../components/multiline-text';
import TelegramIcon from '@mui/icons-material/Telegram';
import GitHubIcon from '@mui/icons-material/GitHub';
import EmailIcon from '@mui/icons-material/Email';
import Chip from '@mui/material/Chip';
import { ThemeProvider } from '@mui/material';
import { MyTheme } from '../theme-mui';

export default function AboutPage() {
  return (
    <div
      className="p-10 mt-5 w-5/6 bg-my-third-color drop-shadow-2xl rounded-md"
    >
      <Text size="large" className="mb-5">О сайте</Text>

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{fontWeight: 600, fontSize: "var(--my-medium-size)"}}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          {"Информация"}
        </AccordionSummary>
        <AccordionDetails>
          <Text size="medium">
            Сайт предназначен для бронирования книг в библиотеках вашего города.
          </Text>
        </AccordionDetails>
      </Accordion>

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{fontWeight: 600, fontSize: "var(--my-medium-size)"}}
          aria-controls="panel2-content"
          id="panel2-header"
        >
          {"Правила бронирования"}
        </AccordionSummary>
        <AccordionDetails>
          <MultilineText
            size="medium"
          >
            {"1. При взятии книги указывается четкая дата ее возврата."}
            {"2. Если возврат книги происходит вовремя, то рейтинг читателя увеличивается на 1 пункт \
              и он может брать на руки больше книг (равное количеству его рейтинга)."}
            {"3. Если возврат книги происходит позже указанного времени, то рейтинг пользователя \
            понижается на 10 пунктов."}
            {"4. При возврате книги пользователь указывает внешнее состояние книги и если оно \
            отличается от изначального, то рейтинг пользователя понижается на 10 пунктов."}
            {"5. Пользователь при возврате должен указать верное состояние книги."}
            {"6. Если рейтинг пользователя достиг 0 или отрицательного значения, то\
            необходимо обратиться к администратору по контактам, указанным в разделе ниже."}
          </MultilineText>
        </AccordionDetails>
      </Accordion>

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          sx={{fontWeight: 600, fontSize: "var(--my-medium-size)"}}
          aria-controls="panel2-content"
          id="panel2-header"
        >
          {"Контакты"}
        </AccordionSummary>
        <AccordionDetails className="flex flex-row gap-5 justify-center">
          <ThemeProvider theme={MyTheme}>
            <Chip
              color="secondary"
              size="medium"
              icon={<GitHubIcon />}
              label="@amunra2"
              component="a"
              target="_blank"
              rel="noopener noreferrer"
              href="https://github.com/amunra2"
              clickable
            />
            <Chip
              color="secondary"
              icon={<TelegramIcon />}
              label="@amunra2"
              component="a"
              target="_blank"
              rel="noopener noreferrer"
              href="https://t.me/amunra2"
              clickable
            />
            <Chip
              color="secondary"
              icon={<EmailIcon />}
              label="ivancvet2001@gmail.com"
            />
          </ThemeProvider>
        </AccordionDetails>
      </Accordion>
    </div>
  )
}
