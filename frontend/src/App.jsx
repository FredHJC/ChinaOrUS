import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import Landing from './pages/Landing';
import Questionnaire from './pages/Questionnaire';
import Result from './pages/Result';

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/questionnaire" element={<Questionnaire />} />
          <Route path="/result/:sessionId" element={<Result />} />
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
