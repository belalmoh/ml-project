import React, { useEffect } from 'react';
import Button from "@material-ui/core/Button";
import CircularProgress from '@material-ui/core/CircularProgress';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';

import Papa from 'papaparse';

import Table from '../../components/table';
import Modal from '../../components/modal';

export default function Movies({data}) {
  const [open, setOpen] = React.useState(false);
  const [progress, setProgress] = React.useState(false);
  const [movieId, setMovieId] = React.useState(false);
  const [kNeighbors, setKNeighbors] = React.useState(5);

  const [knnResult, setKnnResult] = React.useState([]);

  const handleOpen = (movieId) => {
    setOpen(true);
    setMovieId(movieId);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleKNeighborsChange = ({target: {value}}) => {
    setKNeighbors(value);
  }

  useEffect(() => {
    setKnnResult([]);
  }, [movieId, kNeighbors])
  
  const getSimilarMoviesUsingKNN = () => {
    setProgress(true);
    setKnnResult([]);
    Papa.parse(`http://localhost:5000/api/algorithm/collab/movie/${movieId}/${kNeighbors}`, {
      download: true,
      complete: (results, file) => {
        setProgress(false);
        let result = JSON.parse(results.data);
        setKnnResult([...knnResult, ...result])
      }
    })
  }

  const options = {
    filterType: 'checkbox',
    filter: false,
    print: false,
    selectableRows: "none"
  };

  const columns = [
    {name: "movieId", label: "Movie ID"}, 
    {name: "title", label: "Title"}, 
    {name: "genres", label: "Genres"},
    {name: "Actions", options: {
        customBodyRender: (value, tableMeta, updateValue) => {
          return (
            <div>
              <Button variant="outlined" color="secondary" onClick={() => handleOpen(tableMeta.rowData[0])}>
                {`Find Similar`}
              </Button>
              <Modal open={open} handleClose={handleClose}>
                  <div>
                    <h2 id="transition-modal-title">Collaborative Approach</h2>
                    <Grid container spacing={6}>
                      <Grid item xs={6}>
                        <Button variant="outlined" color="secondary" onClick={() => getSimilarMoviesUsingKNN()}>
                          {progress ? 
                            <CircularProgress color="secondary" size={25} /> : `KNN` 
                          }
                        </Button>
                        <br />
                        <TextField id="standard-basic" label="K Value" onChange={handleKNeighborsChange} defaultValue={kNeighbors} disabled={progress}/>
                      </Grid>
                    </Grid>
                    <br />
                    {knnResult.length > 0 && !progress ? 
                      <Movies data={knnResult}/>
                      :
                      ''
                    }
                  </div>
              </Modal>
            </div>
          );
        }
      }}
  ];

  return (
    <Table data={data} 
        options={options} 
        title={"Movies"} 
        columns={columns} 
    />
  );
}
