import React, { useState } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [url, setUrl] = useState("");
  const [format, setFormat] = useState("mp3");
  const [quality, setQuality] = useState("high");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [downloadReady, setDownloadReady] = useState(false);
  const [downloadData, setDownloadData] = useState(null);

  const formatOptions = [
    { value: "mp3", label: "MP3" },
    { value: "wav", label: "WAV" },
    { value: "m4a", label: "M4A" },
    { value: "flac", label: "FLAC" },
    { value: "ogg", label: "OGG" }
  ];

  const qualityOptions = [
    { value: "high", label: "High Quality (Best Available)" },
    { value: "medium", label: "Medium Quality (128kbps)" },
    { value: "low", label: "Low Quality (64kbps)" }
  ];

  const isValidYouTubeUrl = (url) => {
    return url.includes('youtube.com') || url.includes('youtu.be');
  };

  const handleDownload = async () => {
    if (!url.trim()) {
      setMessage("Please enter a YouTube URL");
      return;
    }

    if (!isValidYouTubeUrl(url)) {
      setMessage("Please enter a valid YouTube URL");
      return;
    }

    setLoading(true);
    setMessage("Processing your request...");
    setDownloadReady(false);
    setDownloadData(null);

    try {
      const response = await axios.post(`${API}/download`, {
        url: url.trim(),
        format: format,
        quality: quality
      });

      if (response.data.success) {
        setMessage(`Successfully processed: ${response.data.title}`);
        setDownloadData(response.data);
        setDownloadReady(true);
        
        // Trigger direct download
        const encodedPath = response.data.file_path.replace(/\//g, "__");
        const downloadUrl = `${API}/download-file/${encodedPath}`;
        
        // Create a temporary link and click it to trigger download
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `${response.data.title}.${format}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
      } else {
        setMessage(`Error: ${response.data.message}`);
      }
    } catch (error) {
      console.error('Download error:', error);
      if (error.response?.data?.detail) {
        setMessage(`Error: ${error.response.data.detail}`);
      } else {
        setMessage("An error occurred while processing your request. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setUrl("");
    setMessage("");
    setDownloadReady(false);
    setDownloadData(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">
              YouTube Audio Downloader
            </h1>
            <p className="text-xl text-blue-200">
              Convert YouTube videos to high-quality audio files
            </p>
          </div>

          {/* Main Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
            <div className="space-y-6">
              {/* URL Input */}
              <div>
                <label className="block text-white font-semibold mb-3 text-lg">
                  YouTube URL
                </label>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all"
                  disabled={loading}
                />
              </div>

              {/* Format and Quality Selection */}
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-white font-semibold mb-3 text-lg">
                    Audio Format
                  </label>
                  <select
                    value={format}
                    onChange={(e) => setFormat(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all"
                    disabled={loading}
                  >
                    {formatOptions.map((option) => (
                      <option key={option.value} value={option.value} className="bg-gray-800">
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-white font-semibold mb-3 text-lg">
                    Audio Quality
                  </label>
                  <select
                    value={quality}
                    onChange={(e) => setQuality(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all"
                    disabled={loading}
                  >
                    {qualityOptions.map((option) => (
                      <option key={option.value} value={option.value} className="bg-gray-800">
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Download Button */}
              <div className="text-center">
                <button
                  onClick={handleDownload}
                  disabled={loading || !url.trim()}
                  className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-500 disabled:to-gray-600 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed shadow-lg"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                      Processing...
                    </div>
                  ) : (
                    "Download Audio"
                  )}
                </button>
              </div>

              {/* Status Message */}
              {message && (
                <div className={`text-center p-4 rounded-xl ${
                  message.includes('Error') 
                    ? 'bg-red-500/20 text-red-200 border border-red-500/30' 
                    : 'bg-green-500/20 text-green-200 border border-green-500/30'
                }`}>
                  <p className="font-medium">{message}</p>
                </div>
              )}

              {/* Download Complete */}
              {downloadReady && downloadData && (
                <div className="bg-green-500/20 border border-green-500/30 rounded-xl p-6 text-center">
                  <div className="text-green-200 mb-4">
                    <svg className="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h3 className="text-xl font-semibold mb-2">Download Complete!</h3>
                    <p className="text-green-300 mb-4">Your audio file should start downloading automatically</p>
                  </div>
                  
                  <button
                    onClick={handleReset}
                    className="bg-white/20 hover:bg-white/30 text-white font-medium py-2 px-6 rounded-lg transition-all"
                  >
                    Download Another
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Features */}
          <div className="mt-12 grid md:grid-cols-3 gap-6">
            <div className="text-center text-white">
              <div className="bg-white/10 rounded-2xl p-6 backdrop-blur-sm">
                <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Multiple Formats</h3>
                <p className="text-blue-200">Support for MP3, WAV, M4A, FLAC, and OGG formats</p>
              </div>
            </div>
            
            <div className="text-center text-white">
              <div className="bg-white/10 rounded-2xl p-6 backdrop-blur-sm">
                <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">High Quality</h3>
                <p className="text-blue-200">Choose from multiple quality options for best results</p>
              </div>
            </div>
            
            <div className="text-center text-white">
              <div className="bg-white/10 rounded-2xl p-6 backdrop-blur-sm">
                <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Safe & Secure</h3>
                <p className="text-blue-200">No data stored, direct download to your device</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
