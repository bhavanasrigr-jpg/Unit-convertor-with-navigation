
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Unit Converter',
      theme: ThemeData(
        colorSchemeSeed: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

// HOME SCREEN

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final converters = {
      'Length': ['Meters', 'Kilometers', 'Centimeters', 'Feet', 'Inches'],
      'Weight': ['Kilograms', 'Grams', 'Milligrams', 'Pounds', 'Ounces'],
      'Temperature': ['Celsius', 'Fahrenheit', 'Kelvin'],
    };

    return Scaffold(
      appBar: AppBar(
        title: const Text('Unit Converter'),
        centerTitle: true,
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.calculate,
              size: 80,
              color: Colors.deepPurple,
            ),
            const SizedBox(height: 15),
            const Text(
              'Choose a Converter',
              style: TextStyle(
                fontSize: 23,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 25),

            ...converters.entries.map((entry) {
              return Card(
                margin: const EdgeInsets.only(bottom: 15),
                child: ListTile(
                  leading: Icon(
                    entry.key == 'Length'
                        ? Icons.straighten
                        : entry.key == 'Weight'
                            ? Icons.monitor_weight
                            : Icons.thermostat,
                    color: Colors.deepPurple,
                    size: 30,
                  ),
                  title: Text(entry.key),
                  trailing: const Icon(Icons.arrow_forward_ios),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => ConverterScreen(
                          title: entry.key,
                          units: entry.value,
                        ),
                      ),
                    );
                  },
                ),
              );
            }),
          ],
        ),
      ),
    );
  }
}

// REUSABLE CONVERTER SCREEN

class ConverterScreen extends StatefulWidget {
  final String title;
  final List<String> units;

  const ConverterScreen({
    super.key,
    required this.title,
    required this.units,
  });

  @override
  State<ConverterScreen> createState() => _ConverterScreenState();
}

class _ConverterScreenState extends State<ConverterScreen> {
  final TextEditingController controller = TextEditingController();

  String? fromUnit;
  String? toUnit;
  String result = '';

  // CONVERSION FUNCTIONS

  double convert(double value, String from, String to) {
    if (from == to) return value;

    // LENGTH
    if (widget.title == 'Length') {
      const factors = {
        'Meters': 1.0,
        'Kilometers': 1000.0,
        'Centimeters': 0.01,
        'Feet': 0.3048,
        'Inches': 0.0254,
      };

      return value * factors[from]! / factors[to]!;
    }

    // WEIGHT
    if (widget.title == 'Weight') {
      const factors = {
        'Kilograms': 1.0,
        'Grams': 0.001,
        'Milligrams': 0.000001,
        'Pounds': 0.45359237,
        'Ounces': 0.028349523125,
      };

      return value * factors[from]! / factors[to]!;
    }

    // TEMPERATURE
    double celsius;

    switch (from) {
      case 'Fahrenheit':
        celsius = (value - 32) * 5 / 9;
        break;
      case 'Kelvin':
        celsius = value - 273.15;
        break;
      default:
        celsius = value;
    }

    switch (to) {
      case 'Fahrenheit':
        return (celsius * 9 / 5) + 32;
      case 'Kelvin':
        return celsius + 273.15;
      default:
        return celsius;
    }
  }

  void performConversion() {
    double? value = double.tryParse(controller.text);

    if (value == null || fromUnit == null || toUnit == null) {
      setState(() {
        result = 'Please enter a valid value and select units.';
      });
      return;
    }

    if (widget.title == 'Temperature' &&
        fromUnit == 'Kelvin' && value < 0) {
      setState(() {
        result = 'Kelvin cannot be negative.';
      });
      return;
    }

    if (widget.title == 'Temperature' &&
        fromUnit == 'Celsius' && value < -273.15) {
      setState(() {
        result = 'Below absolute zero is not valid.';
      });
      return;
    }

    if (widget.title == 'Temperature' &&
        fromUnit == 'Fahrenheit' && value < -459.67) {
      setState(() {
        result = 'Below absolute zero is not valid.';
      });
      return;
    }

    double answer = convert(value, fromUnit!, toUnit!);

    setState(() {
      result = '${answer.toStringAsFixed(4)} $toUnit';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.title} Converter'),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
      ),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const SizedBox(height: 20),

            Icon(
              Icons.calculate,
              size: 75,
              color: Colors.deepPurple,
            ),

            const SizedBox(height: 25),

            TextField(
              controller: controller,
              keyboardType: const TextInputType.numberWithOptions(
                decimal: true,
                signed: true,
              ),
              decoration: const InputDecoration(
                labelText: 'Enter Value',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.numbers),
              ),
            ),

            const SizedBox(height: 20),

            DropdownButtonFormField<String>(
              value: fromUnit,
              decoration: const InputDecoration(
                labelText: 'From Unit',
                border: OutlineInputBorder(),
              ),
              items: widget.units.map((unit) {
                return DropdownMenuItem(
                  value: unit,
                  child: Text(unit),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  fromUnit = value;
                });
              },
            ),

            const SizedBox(height: 20),

            const Icon(
              Icons.arrow_downward,
              color: Colors.deepPurple,
              size: 30,
            ),

            const SizedBox(height: 20),

            DropdownButtonFormField<String>(
              value: toUnit,
              decoration: const InputDecoration(
                labelText: 'To Unit',
                border: OutlineInputBorder(),
              ),
              items: widget.units.map((unit) {
                return DropdownMenuItem(
                  value: unit,
                  child: Text(unit),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  toUnit = value;
                });
              },
            ),

            const SizedBox(height: 25),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: performConversion,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.deepPurple,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.all(15),
                ),
                child: const Text(
                  'CONVERT',
                  style: TextStyle(fontSize: 16),
                ),
              ),
            ),

            const SizedBox(height: 25),

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.deepPurple.shade50,
                borderRadius: BorderRadius.circular(15),
              ),
              child: Column(
                children: [
                  const Text(
                    'Conversion Result',
                    style: TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    result.isEmpty ? 'Result will appear here' : result,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 20,
                      color: Colors.deepPurple,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }
}
