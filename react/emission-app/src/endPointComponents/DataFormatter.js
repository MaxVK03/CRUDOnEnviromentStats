const formatData = (data, dataType) => {
  if (dataType === 'CSV') {
    const rows = data.split('\r\n').map(row => row.split(','));
    rows.pop();
    return (
      <div>
        <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(data, null, 2)}</pre>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          {rows.map((rowData, rowIndex) => (
            <tr key={rowIndex} style={{ border: '1px solid black' }}>
              {rowData.map((cellData, colIndex) => {
                const CellElement = rowIndex === 0 ? 'th' : 'td';
                return (
                  <CellElement
                    key={colIndex}
                    style={{
                      padding: '10px',
                      textAlign: 'center',
                      border: '1px solid black',
                    }}
                  >
                    {cellData}
                  </CellElement>
                );
              })}
            </tr>
          ))}
        </table>
      </div>
    );
  }
  else {
    const limitedData = JSON.stringify(data, null, 2);
    return (
    <div style={{ maxHeight: '475px', overflowY: 'auto', whiteSpace: 'pre-wrap' }}>
      {limitedData}
    </div>
    );
  }
};

export default formatData;
