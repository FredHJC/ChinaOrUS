import { Button, Typography, Space, Card } from 'antd';
import { useNavigate } from 'react-router-dom';
import { RocketOutlined, GlobalOutlined, HomeOutlined } from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: 24,
    }}>
      <Card
        style={{
          maxWidth: 680,
          width: '100%',
          borderRadius: 16,
          boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
        }}
        bodyStyle={{ padding: '48px 40px' }}
      >
        <Space direction="vertical" size="large" style={{ width: '100%', textAlign: 'center' }}>
          <div style={{ fontSize: 48 }}>
            <GlobalOutlined style={{ color: '#3b82f6', marginRight: 16 }} />
            <HomeOutlined style={{ color: '#ef4444' }} />
          </div>

          <Title level={2} style={{ margin: 0 }}>
            留学生去留决策量表 <Text style={{ fontSize: 16, color: '#764ba2', fontWeight: 'normal', verticalAlign: 'middle', border: '1px solid #764ba2', borderRadius: 6, padding: '2px 8px' }}>V2</Text>
          </Title>
          <Text type="secondary" style={{ fontSize: 16 }}>
            US vs China Decision Matrix
          </Text>

          <Paragraph style={{ fontSize: 15, textAlign: 'left', lineHeight: 1.8 }}>
            这是一套基于 <Text strong>29 个核心维度</Text> 的科学量化工具，涵盖基础信息、职业财务、身份生活、家庭情感四大领域。
            通过你对每一项的客观现状选择和个人重视程度打分，系统将为你生成一份个性化的去留建议报告。
          </Paragraph>

          <Card
            size="small"
            style={{ background: '#f6f8fc', border: 'none', textAlign: 'left' }}
          >
            <Space direction="vertical" size={4}>
              <Text strong style={{ color: '#764ba2' }}>V2 更新亮点</Text>
              <Text><RocketOutlined style={{ marginRight: 8 }} />29 道决策维度题，新增性别、城市级别、来美年数</Text>
              <Text><RocketOutlined style={{ marginRight: 8 }} />选项全面中立化，大部分题目扩展至 5 档渐变梯度</Text>
              <Text><RocketOutlined style={{ marginRight: 8 }} />全新权重系数体系，更精准反映个人偏好</Text>
              <Text><RocketOutlined style={{ marginRight: 8 }} />四象限可视化散点图 + 精准诊断建议</Text>
            </Space>
          </Card>

          <Button
            type="primary"
            size="large"
            onClick={() => navigate('/questionnaire')}
            style={{
              height: 52,
              fontSize: 18,
              borderRadius: 12,
              paddingInline: 48,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
            }}
          >
            开始测试
          </Button>

          <Text type="secondary" style={{ fontSize: 12 }}>
            预计用时 5-10 分钟 | 结果仅供参考
          </Text>
        </Space>
      </Card>
    </div>
  );
}
