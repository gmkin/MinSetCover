import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class MinSetCover {
	private static List<Integer>[] sets;                // encompasses all sets
	private static int FULLSET;                         // set we are trying to achieve
	private static int maxNum = 0;
	private static List<Integer> best = new ArrayList<>();

	public static void main(String[] args) throws IOException {
		long time = System.nanoTime();
		BufferedReader br = new BufferedReader(new FileReader(args[1]));
		String currentLine;

		maxNum = Integer.parseInt(br.readLine());
		FULLSET = (1 << maxNum) - 1;
		sets = new List[Integer.parseInt(br.readLine())];
		for (int i = 0; i < maxNum; i++)
			sets[i] = new ArrayList<>();

		while ((currentLine = br.readLine()) != null) {
			int setLine = 0;
			for (String str : currentLine.split(" "))
				setLine |= 1 << Integer.parseInt(str) - 1;

			boolean isIn = false;
			for (List<Integer> set : sets) {
				if (set == null)
					continue;
				for (int i = set.size() - 1; i >= 0; i--) {
					int newSet = setLine | set.get(i);  // Union of 2 sets
					if (newSet == setLine)              // oldSet was subset of newSet
						set.remove(i);                  // old set was useless
					if (newSet == set.get(i)) {         // newSet is subset of oldSet
						isIn = true;
						break;
					}
				}
			}

			if (!isIn)
				for (int i = 0; i < maxNum; i++)
					if ((setLine & 1 << i) != 0)
						sets[i].add(setLine);
		}
		br.close();

		List<Integer> res = new ArrayList<>();
		int setCover = 0;
		for (int i = 0; i < maxNum; i++) {              // GOAL: take all singles
			if (sets[i] == null)
				continue;
			switch (sets[i].size()) {
				case 0:
					System.out.printf("Element %d does not exist.  Premature break", i);
					System.exit(1);
					break;
				case 1:
					int set = sets[i].get(0);
					if (!res.contains(set))
						res.add(set);        // single element for set, must take
					setCover |= set;
					break;
			}
		}

		if (setCover == FULLSET)
			printSets(res);

		best.addAll(IntStream.rangeClosed(0, maxNum).boxed().collect(Collectors.toList()));

		for (List<Integer> set : sets)
			if (set != null)
				for (int i = set.size() -1; i >= 0; i--)
					if ((setCover | set.get(i)) == setCover)
						set.remove(i);

		printSets(res);

		// self purging trees
		attemptCoverSet(setCover, 0, 0, new ArrayList<>(res));
		printSets(best);

		System.out.println(System.nanoTime() - time);
	}

	private static void attemptCoverSet(int setCover, int startPos, int depth, List<Integer> data) {
		if (depth >= best.size() || data.size() >= best.size())
			return;
		if (setCover == FULLSET) {
			best = new ArrayList<>(data);
			printSets(best);
			return;
		}
		for (int i = startPos; i < maxNum; i++) {
			if ((setCover | 1 << i) == setCover)
				continue;
			for (int k : sets[i]) {
				data.add(k);
				attemptCoverSet(setCover | k, startPos + 1, depth + 1, data);
				data.remove(data.size()-1);
			}
		}
	}

	private static void printSets(List<Integer> res) {
		System.out.println("-------------------------------------");
		for (int val : res) {
			for (int i = 0; i < maxNum; i++)
				if ((val | 1 << i) == val)
					System.out.printf("%03d ", i + 1);
			System.out.println();
		}
	}
}
