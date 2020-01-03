import React, { useEffect } from 'react';
import Button from "@material-ui/core/Button";
import Papa from 'papaparse';

import Table from '../../components/table'

export default function Movies({data}) {
  
  const getSimilarMoviesUsingKNN = (movieId) => {
    Papa.parse(`http://localhost:5000/api/algorithm/collab/movie/${movieId}/5`, {
      download: true,
      complete: (results, file) => {
        let result = JSON.parse(results.data);
        console.log(result);
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
            <Button variant="outlined" color="secondary" onClick={() => getSimilarMoviesUsingKNN(tableMeta.rowData[0])}>
              {`Find Similar`}
            </Button>
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
