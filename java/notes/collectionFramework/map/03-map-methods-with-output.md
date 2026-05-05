# 03 - Map Methods With Printed Output

Use this file as your method practice sheet.

```java
import java.util.*;

public class MapMethodsDemo {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();

        // put
        System.out.println("put Ram->80: " + map.put("Ram", 80));
        System.out.println("put Sita->92: " + map.put("Sita", 92));
        System.out.println("put Ram->95 (old value returned): " + map.put("Ram", 95));

        // get and getOrDefault
        System.out.println("get Ram: " + map.get("Ram"));
        System.out.println("get Shyam: " + map.get("Shyam"));
        System.out.println("getOrDefault Shyam,0: " + map.getOrDefault("Shyam", 0));

        // contains
        System.out.println("containsKey Sita: " + map.containsKey("Sita"));
        System.out.println("containsValue 92: " + map.containsValue(92));

        // size and isEmpty
        System.out.println("size: " + map.size());
        System.out.println("isEmpty: " + map.isEmpty());

        // putIfAbsent
        System.out.println("putIfAbsent Sita->100 (existing value returned): " + map.putIfAbsent("Sita", 100));
        System.out.println("putIfAbsent Laxman->88 (null returned): " + map.putIfAbsent("Laxman", 88));

        // replace
        System.out.println("replace Ram->99 (old value): " + map.replace("Ram", 99));
        System.out.println("replace Ram 99->100 (success?): " + map.replace("Ram", 99, 100));

        // remove
        System.out.println("remove Sita: " + map.remove("Sita"));
        System.out.println("remove Ram,999 (success?): " + map.remove("Ram", 999));

        // computeIfAbsent
        map.computeIfAbsent("IT", k -> 50);
        System.out.println("after computeIfAbsent IT: " + map);

        // computeIfPresent
        map.computeIfPresent("IT", (k, v) -> v + 10);
        System.out.println("after computeIfPresent IT+10: " + map);

        // compute
        map.compute("IT", (k, v) -> v == null ? 1 : v * 2);
        System.out.println("after compute IT*2: " + map);

        // merge
        map.merge("IT", 5, Integer::sum);
        map.merge("NEW", 1, Integer::sum);
        System.out.println("after merge IT and NEW: " + map);

        // keySet, values, entrySet
        System.out.println("keys: " + map.keySet());
        System.out.println("values: " + map.values());
        System.out.println("entries: " + map.entrySet());

        // replaceAll
        map.replaceAll((k, v) -> v + 1);
        System.out.println("after replaceAll +1: " + map);

        // clear
        map.clear();
        System.out.println("after clear: " + map);
        System.out.println("isEmpty after clear: " + map.isEmpty());
    }
}
```

Expected output (order may vary in `HashMap` print):

```text
put Ram->80: null
put Sita->92: null
put Ram->95 (old value returned): 80
get Ram: 95
get Shyam: null
getOrDefault Shyam,0: 0
containsKey Sita: true
containsValue 92: true
size: 2
isEmpty: false
putIfAbsent Sita->100 (existing value returned): 92
putIfAbsent Laxman->88 (null returned): null
replace Ram->99 (old value): 95
replace Ram 99->100 (success?): true
remove Sita: 92
remove Ram,999 (success?): false
after computeIfAbsent IT: {IT=50, Ram=100, Laxman=88}
after computeIfPresent IT+10: {IT=60, Ram=100, Laxman=88}
after compute IT*2: {IT=120, Ram=100, Laxman=88}
after merge IT and NEW: {IT=125, NEW=1, Ram=100, Laxman=88}
keys: [IT, NEW, Ram, Laxman]
values: [125, 1, 100, 88]
entries: [IT=125, NEW=1, Ram=100, Laxman=88]
after replaceAll +1: {IT=126, NEW=2, Ram=101, Laxman=89}
after clear: {}
isEmpty after clear: true
```

Important: `HashMap` does not guarantee print order.
If you need stable order for teaching output, use `LinkedHashMap`.
