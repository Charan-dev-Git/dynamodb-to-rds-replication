resource "aws_cloudwatch_event_rule" "user_processor_schedule" {
  name                = local.scheduler_name
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.user_processor_schedule.name
  target_id = "user-processor"
  arn       = aws_lambda_function.user_processor.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.user_processor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.user_processor_schedule.arn
}