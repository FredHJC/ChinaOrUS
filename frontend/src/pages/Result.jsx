import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useState, useEffect, useRef } from 'react';
import { Button, Card, Typography, Space, Spin, Tag, QRCode, message } from 'antd';
import { CameraOutlined, RedoOutlined, GlobalOutlined, HomeOutlined } from '@ant-design/icons';
import html2canvas from 'html2canvas';
import ScatterChart from '../components/ScatterChart';
import { getResult, getScatterData } from '../api';

const { Title, Paragraph, Text } = Typography;

const QUADRANT_STYLES = {
  us_high_cn_low: { color: '#3b82f6', icon: <GlobalOutlined />, tagColor: 'blue' },
  us_low_cn_high: { color: '#ef4444', icon: <HomeOutlined />, tagColor: 'red' },
  us_high_cn_high: { color: '#a855f7', icon: <GlobalOutlined />, tagColor: 'purple' },
  us_low_cn_low: { color: '#6b7280', icon: null, tagColor: 'default' },
};

export default function Result() {
  const { sessionId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [data, setData] = useState(location.state || null);
  const [allPoints, setAllPoints] = useState([]);
  const [loading, setLoading] = useState(!location.state);
  const [exporting, setExporting] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  const exportRef = useRef(null);

  useEffect(() => {
    getScatterData().then(setAllPoints).catch(() => {});
  }, []);

  useEffect(() => {
    if (!data && sessionId) {
      getResult(sessionId).then((res) => {
        setData({
          session_id: res.session_id,
          quadrant: res.quadrant,
          quadrant_label: res.quadrant_label,
          diagnosis: res.diagnosis,
          chart_data: res.chart_data,
        });
        setLoading(false);
      });
    }
  }, [sessionId, data]);

  const handleExportImage = async () => {
    if (!exportRef.current) return;
    setExporting(true);
    try {
      const el = exportRef.current;
      const origStyle = el.style.cssText;

      // Force desktop-width layout off-screen for consistent capture
      const EXPORT_W = 800;
      el.style.cssText = `
        width: ${EXPORT_W}px;
        position: fixed;
        left: -9999px;
        top: 0;
        background: #fff;
        padding: 16px;
      `;

      // Trigger ECharts chart resize to new width
      window.dispatchEvent(new Event('resize'));
      await new Promise((r) => setTimeout(r, 800));

      const rawCanvas = await html2canvas(el, {
        scale: 2,
        backgroundColor: '#ffffff',
        useCORS: true,
        logging: false,
      });

      // Restore original layout immediately
      el.style.cssText = origStyle;
      window.dispatchEvent(new Event('resize'));

      // Create final canvas with 3:4 (width:height) ratio
      const finalW = rawCanvas.width;
      const finalH = Math.max(Math.round(finalW * 4 / 3), rawCanvas.height);
      const finalCanvas = document.createElement('canvas');
      finalCanvas.width = finalW;
      finalCanvas.height = finalH;
      const ctx = finalCanvas.getContext('2d');
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, finalW, finalH);
      // Center content vertically in the 4:3 frame
      const yOffset = Math.round((finalH - rawCanvas.height) / 2);
      ctx.drawImage(rawCanvas, 0, yOffset);

      setPreviewUrl(finalCanvas.toDataURL('image/png'));
    } catch (err) {
      console.error(err);
      message.error('生成图片失败，请重试');
    } finally {
      setExporting(false);
    }
  };

  const handleDownload = () => {
    if (!previewUrl) return;
    const link = document.createElement('a');
    link.download = `决策报告_${data.session_id.slice(0, 8)}.png`;
    link.href = previewUrl;
    link.click();
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!data) return null;

  const style = QUADRANT_STYLES[data.quadrant] || QUADRANT_STYLES.us_low_cn_low;

  return (
    <div style={{
      maxWidth: 800,
      margin: '0 auto',
      padding: '32px 16px',
    }}>
      <Title level={2} style={{ textAlign: 'center', marginBottom: 32 }}>
        测试结果
      </Title>

      <div style={{ textAlign: 'center', marginBottom: 16 }}>
        <Text type="secondary" style={{ fontSize: 12 }}>
          手机端渲染效果可能不佳，建议尝试生成结果图片。
        </Text>
      </div>

      {/* 可导出区域 */}
      <div ref={exportRef} style={{ background: '#fff', padding: 16 }}>
        {/* 导出时显示的标题 */}
        <div style={{ textAlign: 'center', marginBottom: 16 }}>
          <Title level={3} style={{ margin: 0 }}>留学生去留决策量表 V2 - 测试报告</Title>
        </div>

        {/* 四象限图 */}
        <Card style={{ marginBottom: 24, borderRadius: 12 }}>
          <ScatterChart chartData={data.chart_data} quadrant={data.quadrant} allPoints={allPoints} />
        </Card>

        {/* 诊断结果 */}
        <Card
          style={{
            marginBottom: 24,
            borderRadius: 12,
            borderLeft: `4px solid ${style.color}`,
          }}
        >
          <Space direction="vertical" size="middle" style={{ width: '100%' }}>
            <Space>
              <Tag color={style.tagColor} style={{ fontSize: 16, padding: '4px 16px' }}>
                {data.quadrant_label}
              </Tag>
            </Space>
            <Paragraph style={{ fontSize: 15, lineHeight: 1.8, margin: 0 }}>
              {data.diagnosis}
            </Paragraph>
          </Space>
        </Card>

        <div style={{ textAlign: 'center' }}>
          <Text type="secondary" style={{ fontSize: 12 }}>
            本测试结果仅供参考，不构成任何专业建议。人生决策请综合考虑更多因素。
          </Text>
        </div>

        {/* 网站二维码 */}
        <div style={{
          display: 'flex',
          justifyContent: 'flex-end',
          alignItems: 'center',
          marginTop: 20,
          gap: 12,
        }}>
          <div style={{ textAlign: 'right' }}>
            <Text style={{ fontSize: 13, fontWeight: 'bold', display: 'block' }}>
              扫码测一测
            </Text>
            <Text type="secondary" style={{ fontSize: 11 }}>
              chinaorus.com
            </Text>
          </div>
          <QRCode
            value="https://chinaorus.com/"
            size={80}
            bordered={false}
            color="#333"
          />
        </div>
      </div>

      {/* 操作按钮 */}
      <Space size="middle" style={{ display: 'flex', justifyContent: 'center', marginTop: 24 }}>
        <Button
          type="primary"
          size="large"
          icon={<CameraOutlined />}
          loading={exporting}
          onClick={handleExportImage}
          style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
          }}
        >
          生成结果图片
        </Button>
        <Button
          size="large"
          icon={<RedoOutlined />}
          onClick={() => navigate('/questionnaire')}
        >
          重新测试
        </Button>
      </Space>

      {/* 图片预览弹层 */}
      {previewUrl && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.85)',
            zIndex: 1000,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 16,
          }}
          onClick={() => setPreviewUrl(null)}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              maxWidth: '90vw',
              maxHeight: '75vh',
              overflow: 'auto',
              borderRadius: 12,
            }}
          >
            <img
              src={previewUrl}
              alt="测试报告"
              style={{
                width: '100%',
                display: 'block',
                borderRadius: 12,
              }}
            />
          </div>
          <Space size="middle" style={{ marginTop: 16 }}>
            <Button
              type="primary"
              size="large"
              onClick={handleDownload}
            >
              下载图片
            </Button>
            <Button
              size="large"
              style={{ color: '#fff', borderColor: '#fff' }}
              ghost
              onClick={() => setPreviewUrl(null)}
            >
              关闭
            </Button>
          </Space>
          <Text style={{ color: 'rgba(255,255,255,0.6)', marginTop: 12, textAlign: 'center' }}>
            手机用户：长按图片即可保存到相册
          </Text>
        </div>
      )}
    </div>
  );
}
