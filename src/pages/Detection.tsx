// pages/Detection.tsx
import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiUpload, FiMic, FiDownload, FiRefreshCw } from 'react-icons/fi';

interface AnalysisFeature {
  name: string;
  value: number;
}

interface AnalysisResults {
  isDeepfake: boolean;
  confidence: number;
  features: AnalysisFeature[];
}

const Detection = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      analyzeFile(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      analyzeFile(e.dataTransfer.files[0]);
    }
  };

  const analyzeFile = (file: File) => {
    setIsAnalyzing(true);
    // Use the file for actual analysis
    console.log('Analyzing file:', file.name, file.type, file.size);
    
    // Simulate analysis
    setTimeout(() => {
      setIsAnalyzing(false);
      setResults({
        isDeepfake: Math.random() > 0.7,
        confidence: Math.floor(Math.random() * 20) + 80,
        features: [
          { name: "Spectral Consistency", value: Math.floor(Math.random() * 20) + 80 },
          { name: "Micro-timing Analysis", value: Math.floor(Math.random() * 20) + 80 },
          { name: "Vocal Biomarkers", value: Math.floor(Math.random() * 20) + 80 },
          { name: "Synthetic Artifacts", value: Math.floor(Math.random() * 20) + 80 }
        ]
      });
    }, 3000);
  };

  const startRecording = () => {
    setIsRecording(true);
    // Simulate recording
    setTimeout(() => {
      setIsRecording(false);
      const mockFile = new File([""], "recording.wav", { type: "audio/wav" });
      setFile(mockFile);
      analyzeFile(mockFile);
    }, 2000);
  };

  const resetAnalysis = () => {
    setFile(null);
    setResults(null);
  };

  return (
    <div className="container mx-auto px-4 pt-28 py-12">
      <motion.h1 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl md:text-4xl font-bold mb-8 dark:text-white"
      >
        Voice Authenticity Analysis
      </motion.h1>

      <AnimatePresence mode="wait">
        {!file && !results && (
          <motion.div
            key="upload"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 md:p-12 mb-8 border border-gray-100 dark:border-gray-700"
          >
            <div 
              className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-12 text-center cursor-pointer hover:border-blue-500 transition-all duration-300"
              onClick={() => fileInputRef.current?.click()}
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
            >
              <FiUpload className="mx-auto w-12 h-12 text-gray-400 mb-4" />
              <h3 className="text-xl font-semibold mb-2 dark:text-white">Upload Voice Sample</h3>
              <p className="text-gray-500 dark:text-gray-400 mb-4">Drag & drop an audio file here, or click to browse</p>
              <button className="px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg text-sm font-medium">
                Select File
              </button>
              <input 
                type="file" 
                ref={fileInputRef}
                onChange={handleFileChange}
                accept="audio/*"
                className="hidden" 
              />
            </div>

            <div className="mt-8 text-center">
              <p className="text-gray-500 dark:text-gray-400 mb-4">Or record directly</p>
              <motion.button
                whileTap={{ scale: 0.95 }}
                className={`relative w-24 h-24 rounded-full flex items-center justify-center mx-auto shadow-lg ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-blue-600 hover:bg-blue-700'} transition-all duration-300 text-white`}
                onClick={startRecording}
                disabled={isRecording}
              >
                <FiMic className="w-8 h-8" />
                {isRecording && (
                  <motion.div 
                    className="absolute inset-0 rounded-full border-4 border-red-500 opacity-0"
                    animate={{ 
                      scale: [1, 1.5],
                      opacity: [0.7, 0]
                    }}
                    transition={{ 
                      duration: 1.5,
                      repeat: Infinity,
                      ease: "easeOut"
                    }}
                  />
                )}
              </motion.button>
            </div>
          </motion.div>
        )}

        {isAnalyzing && (
          <motion.div
            key="analyzing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 md:p-12 mb-8 border border-gray-100 dark:border-gray-700 text-center"
          >
            <div className="mb-6">
              <div className="relative w-24 h-24 mx-auto mb-4">
                <div className="absolute inset-0 rounded-full bg-blue-100 dark:bg-blue-900 animate-ping opacity-75"></div>
                <div className="absolute inset-2 rounded-full bg-blue-200 dark:bg-blue-800 flex items-center justify-center">
                  <svg className="w-12 h-12 text-blue-600 dark:text-blue-300 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
              </div>
              <h3 className="text-2xl font-semibold mb-2 dark:text-white">Analyzing Voice Sample</h3>
              <p className="text-gray-500 dark:text-gray-400">Our AI is examining spectral patterns and vocal biomarkers...</p>
            </div>

            <div className="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2.5">
              <motion.div 
                className="bg-blue-600 h-2.5 rounded-full" 
                initial={{ width: 0 }}
                animate={{ width: "100%" }}
                transition={{ duration: 3 }}
              />
            </div>
          </motion.div>
        )}

        {results && (
          <motion.div
            key="results"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 md:p-12 mb-8 border border-gray-100 dark:border-gray-700"
          >
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
              <div>
                <h3 className="text-2xl font-semibold dark:text-white">Analysis Results</h3>
                <p className="text-gray-500 dark:text-gray-400">Detailed authenticity assessment</p>
              </div>
              <button 
                onClick={resetAnalysis}
                className="flex items-center px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg text-sm font-medium mt-4 md:mt-0 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                <FiRefreshCw className="mr-2" /> Analyze Another
              </button>
            </div>

            <div className={`p-6 rounded-xl mb-8 ${results.isDeepfake ? 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800' : 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'} border`}>
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-lg font-semibold dark:text-white">
                    {results.isDeepfake ? 'Potential Deepfake Detected' : 'Authentic Voice Sample'}
                  </h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Confidence: {results.confidence}%
                  </p>
                </div>
                <div className={`px-4 py-2 rounded-full text-sm font-medium ${results.isDeepfake ? 'bg-red-100 dark:bg-red-800 text-red-800 dark:text-red-100' : 'bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-100'}`}>
                  {results.isDeepfake ? 'High Risk' : 'Low Risk'}
                </div>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6 mb-8">
              {results.features.map((feature, index) => (
                <div key={index} className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium dark:text-gray-300">{feature.name}</span>
                    <span className="text-sm font-semibold dark:text-white">{feature.value}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${feature.value > 85 ? 'bg-green-500' : feature.value > 70 ? 'bg-yellow-500' : 'bg-red-500'}`}
                      style={{ width: `${feature.value}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>

            <div className="border-t border-gray-100 dark:border-gray-700 pt-6">
              <h4 className="text-lg font-semibold mb-4 dark:text-white">Recommended Actions</h4>
              <div className="space-y-3">
                <p className="text-gray-600 dark:text-gray-300">
                  {results.isDeepfake ? (
                    <>
                      <span className="font-medium">Warning:</span> This voice sample shows strong indicators of synthetic manipulation. 
                      We recommend verifying the source and requesting additional authentication.
                    </>
                  ) : (
                    <>
                      This voice sample appears authentic with high confidence. 
                      No additional verification is recommended at this time.
                    </>
                  )}
                </p>
              </div>
            </div>

            <div className="mt-8 flex flex-wrap gap-4">
              <button className="flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
                <FiDownload className="mr-2" /> Download Full Report
              </button>
              <button className="flex items-center px-6 py-3 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg font-medium transition-colors">
                Share Results
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Detection;