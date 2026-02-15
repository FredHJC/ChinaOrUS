import { Card, Radio, Space, Slider, InputNumber, Typography } from 'antd';

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
      {isAge ? (
        <div style={{ marginBottom: 24 }}>
          <Text style={{ display: 'block', marginBottom: 12 }}>{question.description}</Text>
          <InputNumber
            min={question.min_age}
            max={question.max_age}
            value={answer?.age}
            onChange={handleAgeChange}
            style={{ width: 200 }}
            placeholder="请输入年龄"
            size="large"
          />
        </div>
      ) : (
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
    </Card>
  );
}
