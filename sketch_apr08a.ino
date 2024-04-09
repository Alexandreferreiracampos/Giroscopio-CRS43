const int gyroPin = 34;             // Pino analógico conectado ao giroscópio no ESP32
float supplyVoltage = 5;          // Tensão de alimentação aplicada ao giroscópio em volts (típico para ESP32)
float gyroSensitivity = 1.0;        // Sensibilidade do giroscópio em graus por volt (exemplo)
float gyroOutputVoltage;            // Tensão de saída do giroscópio em volts
float angularRate;                  // Taxa angular medida pelo giroscópio em graus por segundo

void setup() {
  Serial.begin(115200);             // Inicia a comunicação serial com uma taxa de 115200 bps
}

void loop() {
  int gyroValue = analogRead(gyroPin);         // Lê o valor analógico do giroscópio
  gyroOutputVoltage = (gyroValue / 4095.0) * supplyVoltage;  // Calcula a tensão de saída do giroscópio (4095 é o valor máximo de 12 bits)
  angularRate = gyroOutputVoltage * gyroSensitivity;  // Converte a tensão de saída do giroscópio para taxa angular
  
  Serial.print("Valor do Giroscopio: ");
  Serial.print(gyroValue);
  Serial.print(", Movimento: ");
  if(gyroValue > 2900){
    Serial.println(" Direita");
  }else if(gyroValue < 2600){
    Serial.println(" Esquerda");
  }else{
    Serial.println(" Parado!");
  }
  
  delay(1);  // Aguarda 1 segundo antes de realizar a próxima leitura
}
