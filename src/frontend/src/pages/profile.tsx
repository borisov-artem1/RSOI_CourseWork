import Text from '../components/text';
import Avatar from '@mui/material/Avatar';
import UserService from '../services/user-service';
import { useCallback, useEffect, useState } from 'react';
import { UserInterface } from '../model/interface/user.interface';
import { fontSize } from '@mui/system';
import MyAvatar from '../components/avatar';
import AuthService from '../services/auth-service';
import UserCard from '../components/user-card';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import GatewayService from '../services/gateway-service';
import { RatingInterface } from '../model/interface/rating.interface';
import Alert from '@mui/material/Alert';

import { styled } from '@mui/material/styles';
import Rating, { IconContainerProps } from '@mui/material/Rating';
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';
import SentimentDissatisfiedIcon from '@mui/icons-material/SentimentDissatisfied';
import SentimentSatisfiedIcon from '@mui/icons-material/SentimentSatisfied';
import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAltOutlined';
import SentimentVerySatisfiedIcon from '@mui/icons-material/SentimentVerySatisfied';
import { useNavigate } from 'react-router-dom';

const StyledRating = styled(Rating)(({ theme }) => ({
  '& .MuiRating-iconEmpty .MuiSvgIcon-root': {
    color: theme.palette.action.disabled,
  },
}));

const customIcons: {
  [index: string]: {
    icon: React.ReactElement<any>;
    label: string;
  };
} = {
  1: {
    icon: <SentimentVeryDissatisfiedIcon fontSize="large"  color="error" />,
    label: 'Очень плохо',
  },
  2: {
    icon: <SentimentDissatisfiedIcon fontSize="large" color="error" />,
    label: 'Плохо',
  },
  3: {
    icon: <SentimentSatisfiedIcon fontSize="large" color="warning" />,
    label: 'Нормально',
  },
  4: {
    icon: <SentimentSatisfiedAltIcon fontSize="large" color="success" />,
    label: 'Хорошо',
  },
  5: {
    icon: <SentimentVerySatisfiedIcon fontSize="large" color="success" />,
    label: 'Очень хорошо',
  },
};

function IconContainer(props: IconContainerProps) {
  const { value, ...other } = props;
  return <span {...other}>{customIcons[value].icon}</span>;
}

function getRatingStateFromUserRating(stars: number) {
  if (stars <= 0) {
    return 0;
  } else if (stars <= 40) {
    return 1;
  } else if (stars <= 40) {
    return 2;
  } else if (stars <= 60) {
    return 3;
  } else if (stars <= 80) {
    return 4;
  } else {
    return 5;
  }
}


export default function ProfilePage() {
  const [user, setUser] = useState<UserInterface>();
  const [rating, setRating] = useState<RatingInterface>();
  const [ratingState, setRatingState] = useState<number>(0);  
  const [errorUserMsg, setErrorUserMsg] = useState<string>();
  const [errorRatingMsg, setErrorRatingMsg] = useState<string>();
  const navigate = useNavigate();

  const getMe = async () => {
    const user = await UserService.getMe();
    if (user) {
      setUser(user);
      setErrorUserMsg("");
    } else {
      setErrorUserMsg("Ошибка: Не загрузились данные о пользователе");
    }
  };

  const getRating = async () => {
    const rating = await GatewayService.getUserRating();
    if (rating) {
      setRating(rating);
      const rateState = getRatingStateFromUserRating(rating.stars)
      setRatingState(rateState);

      if (rateState === 0) {
        setErrorRatingMsg("Ваш рейтинг слишком низкий. Обратитесь\
          к администратору по контактам, указанным на странице <О сайте>");
      } else {
        setErrorRatingMsg("");
      }
    } else {
      setErrorRatingMsg("Ошибка: Не загрузились данные о рейтинге");
    }
  }

  useEffect(() => {
    if (!AuthService.isAuth()) {
      navigate("/");
    }

    getMe();
    getRating();
  }, []);

  return (
    <div 
      className="flex flex-col p-10 mt-5 w-5/6 bg-my-third-color drop-shadow-2xl rounded-md"
    >
      <Text size="large">Профиль</Text>

      <div className="flex flex-row mt-5 gap-20 items-center">
        <MyAvatar
          size={150}
          lastname={user?.lastname}
          firstname={user?.firstname}
          className="flex-none"
        >
          ?
        </MyAvatar>

        <div className="flex flex-col flex-1">
          <Text
            className="font-extrabold ml-5"
            size="high"
          >
            {user?.login ?? "???"}
          </Text>

          <div className="flex flex-wrap justify-center gap-16">
            <Card
              key="profile"
              raised={true}
              className="mt-5 flex flex-auto justify-center max-w-screen-md"
              sx={{ backgroundColor: "var(--my-third-color)", textWrap: "wrap"}}
            >
              <CardContent>
                <Text className="font-extrabold" size="medium">Обо мне</Text>
                <Divider className="" />
                <UserCard className="mt-3" user={user} useName={false} />

                {errorUserMsg &&
                  <Alert
                    sx={{fontWeight: 1000}}
                    className="mt-5 max-w-80"
                    severity="error"
                  >
                    {errorUserMsg}
                  </Alert>
                }
              </CardContent>
            </Card>

            <Card
              key="rating"
              raised={true}
              className="mt-5 flex flex-auto justify-center max-w-screen-sm"
              sx={{ backgroundColor: "var(--my-third-color)", textWrap: "wrap"}}
            >
              <CardContent>
                <Text className="font-extrabold" size="medium">Рейтинг</Text>
                <Divider />

                <div className="flex flex-col items-center gap-5">
                  <StyledRating
                    className="mt-5"
                    name="text-feedback"
                    readOnly
                    value={ratingState}
                    IconContainerComponent={IconContainer}
                    highlightSelectedOnly
                  />
                  <Text className="font-extrabold" size="high">{rating?.stars}</Text>
                </div>
                
                {errorRatingMsg &&
                  <Alert
                    sx={{fontWeight: 1000}}
                    className="mt-5 max-w-80"
                    severity="error"
                  >
                    {errorRatingMsg}
                  </Alert>
                }
              </CardContent>
            </Card>
          </div>
          
        </div>
      </div>
    </div>
  )
}
