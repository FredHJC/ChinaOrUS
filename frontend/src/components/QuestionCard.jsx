import { Card, Radio, Space, Slider, InputNumber, Typography, Row, Col, Tag } from 'antd';

const { Text } = Typography;

const weightMarks = {
  1: '无所谓',
  2: '不太看重',
  3: '一般',
  4: '比较看重',
  5: '核心诉求',
};

export default function QuestionCard({ question, index, answer, onAnswerChange }) {
  const isAge = question.type === 'age_input';
  const isDual = question.type === 'dual_select';
  const hideWeight = isAge && question.auto_weight;

  const handleOptionChange = (e) => {
    onAnswerChange(question.id, { ...answer, selected_option: e.target.value });
  };

  const handleAgeChange = (value) => {
    if (value !== null) {
      onAnswerChange(question.id, { ...answer, age: value });
    }
  };

  const handleWeightChange = (value) => {
    onAnswerChange(question.id, { ...answer, weight: value });
  };

  const handleUsTierChange = (e) => {
    onAnswerChange(question.id, { ...answer, us_tier: e.target.value });
  };

  const handleCnTierChange = (e) => {
    onAnswerChange(question.id, { ...answer, cn_tier: e.target.value });
  };

  return (
    <Card
      style={{ marginBottom: 24 }}
      title={
        <span>
          <Text type="secondary" style={{ marginRight: 8 }}>Q{index + 1}</Text>
          {question.title}
        </span>
      }
      extra={<Text type="secondary">{question.category}</Text>}
    >
      {isAge && (
        <div style={{ marginBottom: 24 }}>
          <Text style={{ display: 'block', marginBottom: 12 }}>{question.description}</Text>
          <InputNumber
            min={question.min_age}
            value={answer?.age}
            onChange={handleAgeChange}
            style={{ width: 200 }}
            placeholder="请输入年龄（20起）"
            size="large"
          />
        </div>
      )}

      {isDual && (
        <Row gutter={24} style={{ marginBottom: 24 }}>
          <Col xs={24} md={12}>
            <div style={{
              padding: 16,
              background: '#f0f5ff',
              borderRadius: 8,
              border: '1px solid #d6e4ff',
              marginBottom: 12,
            }}>
              <Tag color="blue" style={{ marginBottom: 12, fontSize: 13 }}>
                {question.us_label}
              </Tag>
              <Radio.Group
                value={answer?.us_tier}
                onChange={handleUsTierChange}
                style={{ width: '100%' }}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  {question.us_options.map((opt) => (
                    <Radio
                      key={opt.tier}
                      value={opt.tier}
                      style={{
                        padding: '8px 12px',
                        borderRadius: 6,
                        width: '100%',
                        backgroundColor: answer?.us_tier === opt.tier ? '#bae0ff' : 'transparent',
                      }}
                    >
                      <Text strong style={{ marginRight: 6 }}>{opt.tier}.</Text>
                      {opt.text}
                    </Radio>
                  ))}
                </Space>
              </Radio.Group>
            </div>
          </Col>
          <Col xs={24} md={12}>
            <div style={{
              padding: 16,
              background: '#fff1f0',
              borderRadius: 8,
              border: '1px solid #ffccc7',
              marginBottom: 12,
            }}>
              <Tag color="red" style={{ marginBottom: 12, fontSize: 13 }}>
                {question.cn_label}
              </Tag>
              <Radio.Group
                value={answer?.cn_tier}
                onChange={handleCnTierChange}
                style={{ width: '100%' }}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  {question.cn_options.map((opt) => (
                    <Radio
                      key={opt.tier}
                      value={opt.tier}
                      style={{
                        padding: '8px 12px',
                        borderRadius: 6,
                        width: '100%',
                        backgroundColor: answer?.cn_tier === opt.tier ? '#ffccc7' : 'transparent',
                      }}
                    >
                      <Text strong style={{ marginRight: 6 }}>{opt.tier}.</Text>
                      {opt.text}
                    </Radio>
                  ))}
                </Space>
              </Radio.Group>
            </div>
          </Col>
        </Row>
      )}

      {!isAge && !isDual && (
        <Radio.Group
          value={answer?.selected_option}
          onChange={handleOptionChange}
          style={{ width: '100%', marginBottom: 24 }}
        >
          <Space direction="vertical" style={{ width: '100%' }}>
            {question.options.map((opt) => (
              <Radio
                key={opt.label}
                value={opt.label}
                style={{
                  padding: '12px 16px',
                  border: '1px solid #f0f0f0',
                  borderRadius: 8,
                  width: '100%',
                  transition: 'all 0.2s',
                  backgroundColor: answer?.selected_option === opt.label ? '#e6f4ff' : 'transparent',
                }}
              >
                <Text strong style={{ marginRight: 8 }}>{opt.label}.</Text>
                {opt.text}
              </Radio>
            ))}
          </Space>
        </Radio.Group>
      )}

      {!hideWeight && (
        <div style={{ padding: '0 8px' }}>
          <Text type="secondary" style={{ display: 'block', marginBottom: 8 }}>
            这一项对你有多重要？
          </Text>
          <Slider
            min={1}
            max={5}
            marks={weightMarks}
            value={answer?.weight || 3}
            onChange={handleWeightChange}
            style={{ marginBottom: 0 }}
          />
        </div>
      )}
    </Card>
  );
}
