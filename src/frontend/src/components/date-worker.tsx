import React from 'react'
import { DateValidationError, LocalizationProvider, PickerChangeHandlerContext } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers';
import {Dayjs} from 'dayjs';
import { ThemeProvider } from '@mui/material';
import { MyTheme } from '../theme-mui';

interface DateWorkerProps {
  value: Dayjs | null;
  setValue: (value: Dayjs | null) => void;
  className?: string;
  isReadOnly?: boolean;
}

export default function DateWorker({
  value,
  setValue,
  className,
  isReadOnly = false,
}: DateWorkerProps) {
  const handleChange = (value: Dayjs | null, _: PickerChangeHandlerContext<DateValidationError>) => {
    setValue(value);
  }

  return (
    <ThemeProvider theme={MyTheme}>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DatePicker
          disablePast={true}
          className={className}
          readOnly={isReadOnly}
          format="DD/MM/YYYY"
          value={value}
          onChange={handleChange}
        />
      </LocalizationProvider>
    </ThemeProvider>
  )
}
