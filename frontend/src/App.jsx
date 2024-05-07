import React, { useRef, useState } from "react";
import "./App.css"; // Import the CSS file
import * as FileSaver from "file-saver"; // Import FileSaver.js

const App = () => {
  const hiddenFileInput = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [buttonText, setButtonText] = useState("Select GPKG file"); // Added state for button text

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setButtonText(`Transforming: ${file.name}`); // Update button text
      readFileContent(file); // Read the file content and send to server
    }
  };

  const handleClick = () => {
    hiddenFileInput.current?.click();
  };

  const readFileContent = async (file) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      const base64Content = reader.result.split(",")[1]; // Extract base64 data
      const dataToSend = {
        name: file.name,
        base64src: base64Content,
      };
      sendFileToServer(dataToSend, () => setButtonText("Convert another GPKG")); // Send the constructed JSON object
    };
  };

  const sendFileToServer = async (data, _callback) => {
    try {
      const response = await fetch(
        //"http://127.0.0.1:8000/gpkg", // local
        "https://gpkgtogeojson-backend.fly.dev/gpkg", // prod
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      );

      if (response.ok) {
        console.log("File data sent successfully!");

        // Use FileSaver.js to download the response
        const blob = await response.blob();
        FileSaver.saveAs(blob, "dst.geojson");

        setButtonText("Downloading GeoJSON"); // Update button text for download
      } else {
        console.error("Error sending file data:", response.statusText);
        // Handle any errors that occur during the request
      }
    } catch (error) {
      console.error("Error sending file data:", error);
      // Handle any errors during the fetch operation
    }
    _callback();
  };

  return (
    <div className="App">
      <div className="title">
        <h1>Free GPKG to GeoJSON converter</h1>
      </div>
      <button id="gpkg-file-button" onClick={handleClick}>
        {buttonText}
      </button>
      <input
        type="file"
        ref={hiddenFileInput}
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
      <div className="footer">
        <p>
          Upload a GPKG file, get back back a GeoJSON file. (If you upload a
          large file, it might take a while.)
        </p>
        <p>Suggestions, problems, questions? gpkgtogeojson@protonmail.com</p>
      </div>
    </div>
  );
};

export default App;
