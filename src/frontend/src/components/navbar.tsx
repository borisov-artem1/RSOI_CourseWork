import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import { ThemeProvider } from '@mui/material';
import { MyTheme } from '../theme-mui';
import { WebsiteLogo } from './website-logo';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth-service';
import LoginIcon from '@mui/icons-material/Login';
import Text from './text';

const pages = ['Products', 'Pricing', 'Blog'];
const settings = ['Profile', 'Account', 'Dashboard', 'Logout'];

export default function NavBar() {
  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
  const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);
  const navigate = useNavigate();

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const logoutButtonUserMenu = () => {
    handleCloseUserMenu();
    AuthService.logout();
    navigate("/");
  };

  const goToLoginPage = () => {
    navigate(`/login`);
  }

  const goToProfilePage = () => {
    navigate("/profile");
  }

  const goToAboutPage = () => {
    navigate("/about");
  }

  const goToReservationPage = () => {
    navigate("/reservations");
  }

  const goToStatisticsPage = () => {
    navigate("/statistics");
  }

  return (
    <ThemeProvider theme={MyTheme}>
      <AppBar position="static" color="primary">
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            <WebsiteLogo size="medium" />

            {/* MENU XS SIZE */}
            {/* <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleOpenNavMenu}
                color="inherit"
              >
                <MenuIcon />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorElNav}
                anchorOrigin={{
                  vertical: 'bottom',
                  horizontal: 'left',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'left',
                }}
                open={Boolean(anchorElNav)}
                onClose={handleCloseNavMenu}
                sx={{ display: { xs: 'block', md: 'none' } }}
              >
                {pages.map((page) => (
                  <MenuItem key={page} onClick={handleCloseNavMenu}>
                    <Typography sx={{ textAlign: 'center' }}>{page}</Typography>
                    {page}
                  </MenuItem>
                ))}
              </Menu>
            </Box> */}

            {/* MENU MD SIZE */}
            {/* <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              {pages.map((page) => (
                <Button
                  key={page}
                  onClick={handleCloseNavMenu}
                  sx={{ my: 2, color: 'white', display: 'block' }}
                >
                  {page}
                </Button>
              ))}
            </Box> */}

            {/* USER MENU ALL SIZES */}
            <Box sx={{ marginLeft: "auto", marginRight: 0 }}>
              {AuthService.isAuth() ?
                <Tooltip title="Обо мне">
                  <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                    <AccountBoxIcon 
                      style={{fontSize: `var(--my-large-size)`, lineHeight: `var(--my-large-height)`}}
                      className="text-my-third-color" 
                    />
                  </IconButton>
                </Tooltip>
                :
                <Tooltip title="Войти">
                  <IconButton onClick={goToLoginPage} sx={{ p: 0 }}>
                    <LoginIcon 
                      style={{fontSize: `var(--my-large-size)`, lineHeight: `var(--my-large-height)`}}
                      className="text-my-third-color" 
                    />
                  </IconButton>
                </Tooltip>
              }
              
              {AuthService.isAuth() &&
                <Menu
                  sx={{ mt: '45px' }}
                  id="menu-appbar"
                  anchorEl={anchorElUser}
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorElUser)}
                  onClose={handleCloseUserMenu}
                >
                  <MenuItem onClick={goToProfilePage}>
                    <Text size="little">Профиль</Text>
                  </MenuItem>
                  <MenuItem onClick={goToReservationPage}>
                    <Text size="little">Бронирования</Text>
                  </MenuItem>
                  {AuthService.isAdmin() && 
                    <MenuItem onClick={goToStatisticsPage}>
                      <Text size="little">Статистика</Text>
                    </MenuItem>
                  }
                  <MenuItem onClick={goToAboutPage}>
                    <Text size="little">О сайте</Text>
                  </MenuItem>
                  <MenuItem onClick={logoutButtonUserMenu}>
                    <Text size="little">Выйти</Text>
                  </MenuItem>
                </Menu>
              }
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
    </ThemeProvider>
  );
}
