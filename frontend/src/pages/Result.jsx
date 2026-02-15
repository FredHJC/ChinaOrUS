import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Button, Card, Typography, Space, Spin, Tag } from 'antd';
import { DownloadOutlined, RedoOutlined, GlobalOutlined, HomeOutlined } from '@ant-design/icons';
import ScatterChart from '../components/ScatterChart';
import { getResult, getExportUrl } from '../api';

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
  const [loading, setLoading] = useState(!location.state);

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

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!data) return null;

  const style = QUADRANT_STYLES[data.quadrant] || QUADRANT_STYLES.us_low_cn_low;
  const sid = data.session_id;

  return (
    <div style={{
      maxWidth: 800,
      margin: '0 auto',
      padding: '32px 16px',
    }}>
      <Title level={2} style={{ textAlign: 'center', marginBottom: 32 }}>
        测试结果
      </Title>

      {/* 四象限图 */}
      <Card style={{ marginBottom: 24, borderRadius: 12 }}>
        <ScatterChart chartData={data.chart_data} quadrant={data.quadrant} />
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

      {/* 操作按钮 */}
      <Space size="middle" style={{ display: 'flex', justifyContent: 'center' }}>
        <Button
          type="primary"
          size="large"
          icon={<DownloadOutlined />}
          href={getExportUrl(sid)}
          target="_blank"
          style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
          }}
        >
          导出 PDF 报告
        </Button>
        <Button
          size="large"
          icon={<RedoOutlined />}
          onClick={() => navigate('/questionnaire')}
        >
          重新测试
        </Button>
      </Space>

      <div style={{ textAlign: 'center', marginTop: 32 }}>
        <Text type="secondary">
          本测试结果仅供参考，不构成任何专业建议。人生决策请综合考虑更多因素。
        </Text>
      </div>
    </div>
  );
}
