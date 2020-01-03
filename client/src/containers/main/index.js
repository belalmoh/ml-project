import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

import Papa from 'papaparse';

import Movies from '../movies'

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </Typography>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
  toolbarButtons: {
    marginLeft: "auto",
    marginRight: 0
  },
  menuButton: {
    marginRight: 20,
    marginLeft: 0
  }
}));

export default function Main() {
  const classes = useStyles();
  
  const [value, setValue] = React.useState(0);
  const [users, setUsers] = React.useState([]);
  const [movies, setMovies] = React.useState([]);
  const [ratings, setRatings] = React.useState([]);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };


  // Hook Effect of Users
  useEffect(() => {
    Papa.parse('http://localhost:5000/api/users', {
      download: true,
      complete: (results, file) => {
        let result = JSON.parse(results.data);
        setUsers([...users, ...result])
      }
    })
  }, [])
  
  // Hook Effect of Movies
  useEffect(() => {
    Papa.parse('http://localhost:5000/api/movies', {
      download: true,
      complete: (results, file) => {
        let result = JSON.parse(results.data);
        setMovies([...movies, ...result])
      }
    })
  }, [])

  return (
    <div className={classes.root}>
      <AppBar position="static">
          <Tabs value={value} onChange={handleChange} aria-label="simple tabs example" className={classes.menuButton}>
            <Tab label="Movies" {...a11yProps(0)} />
            <Tab label="Users" {...a11yProps(1)} />
          </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        <Movies data={movies} />
      </TabPanel>
      <TabPanel value={value} index={1}>
      </TabPanel>
    </div>
  );
}
