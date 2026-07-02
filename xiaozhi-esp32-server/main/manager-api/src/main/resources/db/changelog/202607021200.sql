INSERT INTO `ai_model_config` (`id`, `model_type`, `model_code`, `model_name`, `is_default`, `is_enabled`, `config_json`, `doc_link`, `remark`, `sort`, `creator`, `create_date`, `updater`, `update_date`)
SELECT
  'LLM_GitHubModelsLLM',
  'LLM',
  'GitHubModelsLLM',
  'GitHub Models',
  0,
  1,
  '{\"type\": \"openai\", \"model_name\": \"openai/gpt-4.1\", \"base_url\": \"https://models.github.ai/inference\", \"api_key\": \"你的GitHub models:read token\", \"temperature\": 0.7, \"max_tokens\": 500, \"top_p\": 1}',
  'https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models',
  '使用GitHub Models免费实验额度，需填写具备models:read权限的GitHub Token；这不是xiaozhi.me官方云模型代理。',
  16,
  NULL,
  NULL,
  NULL,
  NULL
WHERE NOT EXISTS (
  SELECT 1 FROM `ai_model_config` WHERE `id` = 'LLM_GitHubModelsLLM'
);
